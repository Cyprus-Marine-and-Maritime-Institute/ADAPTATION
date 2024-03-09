from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from dotenv import load_dotenv
from geoalchemy2 import Geometry
import os
import sys

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
LOGS_PATH=os.getenv("LOGS_PATH")
SYS_PATH=os.getenv("SYS_PATH")
sys.path.insert(0, f'{SYS_PATH}')

from AisDb.Models import *
from AisDb.Models.ShipCommonData import ShipCommonData
from AisDb.Models.PositionReport import PositionReport
from AisDb.Models.StaticDataReport import StaticDataReport
from AisDb.Models.StandardClassBPositionReport import StandardClassBPositionReport
from AisDb.Models.ShipStaticData import ShipStaticData
from AisDb.Models.DataLinkManagementMessage import DataLinkManagementMessage
from AisDb.Models.SubscribeMessage import SubscribeMessage
from AisDb.Models.BoundingBox import BoundingBox
from AisDb.Models.FilterShipMMSI import FilterShipMMSI
from AisDb.Models.FilterMessageTypes import FilterMessageTypes
from AisDb.Models.MergedTableResambled import MergedTableResambled
from tqdm import tqdm
from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import array_agg
import pandas as pd
from geoalchemy2.shape import to_shape
from multiprocessing import Pool, cpu_count
from functools import partial as Partial


# Database connection
engine = create_engine(f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
def merge_data_for_mmsi(mmsi,from_time,to_time):

    position_common = session.query(
        ShipCommonData,PositionReport).join(
        PositionReport, ShipCommonData.ShipCommonDataID == PositionReport.ShipCommonDataID).distinct(
            (func.date_trunc('hour', ShipCommonData.TimeUtc) +
    (func.floor(func.extract('minute', ShipCommonData.TimeUtc) / 10) * text("interval '10 minute'"))).label('rounded_time')
            ).filter(
        ShipCommonData.MMSI == mmsi,
        ShipCommonData.TimeUtc >= from_time,
        ShipCommonData.TimeUtc <= to_time
    )
    
    df_pos_common=pd.read_sql(position_common.statement,session.bind)
    # print(df_pos_common.head())
    static_common = session.query(
        ShipCommonData,ShipStaticData).join(
        ShipCommonData, ShipCommonData.ShipCommonDataID == ShipStaticData.ShipCommonDataID).distinct(
        (func.date_trunc('hour', ShipCommonData.TimeUtc)).label('rounded_time')
    ).filter(
        ShipCommonData.MMSI == mmsi,
        ShipCommonData.TimeUtc >= from_time,
        ShipCommonData.TimeUtc <= to_time
    )
    
    df_static_common=pd.read_sql(static_common.statement,session.bind)
    

    if df_pos_common.empty or df_static_common.empty:
        df_pos_common.empty
        print(f"Empty dataframe {df_pos_common.empty}")
        return
    
    df_pos_common['TimeUtc'] = pd.to_datetime(df_pos_common['TimeUtc'])
    df_static_common['TimeUtc'] = pd.to_datetime(df_static_common['TimeUtc'])
    

    df_common=pd.concat([df_pos_common,df_static_common],axis=0).sort_values(by=['TimeUtc'])    

    df_common=df_common.ffill()
    df_common=df_common.bfill()
    # df_common = pd.merge_asof(df_pos_combined, df_static_combined, on='TimeUtc', direction='forward', suffixes=('', '_y'))

    df_common=df_common.dropna()
    
    df_common['Geom']=df_common['Geom'].apply(lambda x: to_shape(x).wkt)
    df_common=df_common[MergedTableResambled.__table__.columns.keys()[1:]]
    df_common.to_sql("mergedtableresambled",engine,if_exists='append',index=False)


def merge_data(from_time=None,to_time=None):
    # Get distinct MMSI from ShipCommonData

    if from_time is None:
        from_time=datetime(1990,1,1,0,0,0)
    if to_time is None:
        to_time=datetime(2050,1,1,0,0,0)

    distinct_mmsi = session.query(
        ShipCommonData.MMSI
    ).group_by(
        ShipCommonData.MMSI
    ).having(
        func.count(ShipCommonData.MMSI) > 10
    ).filter(
        ShipCommonData.MMSI != 0,
    ).all()
    print(f"Found {len(distinct_mmsi)} MMSI")

    mmsi_s=[int(i[0]) for i in distinct_mmsi if len(str(i[0]))>8]
    merge_data_for_mmsi_with_args=Partial(merge_data_for_mmsi,from_time=from_time,to_time=to_time)
    # merge_data_for_mmsi_with_args(mmsi_s[24])
    # return
    with Pool(cpu_count()) as p:
        p.map(merge_data_for_mmsi_with_args,mmsi_s)
        

# Run the merge function
# 2023-11-08 09:28:13.98719
if __name__ == "__main__":
    from_time=datetime(2023,11,8)
    to_time=None
    max_t=session.query(func.max(MergedTableResambled.TimeUtc)).all()
    if max_t[0][0] is not None:
        from_time=max_t[0][0]
    else:
        from_time=None
    merge_data(from_time=None,to_time=to_time)
# Close the session
    session.close()
