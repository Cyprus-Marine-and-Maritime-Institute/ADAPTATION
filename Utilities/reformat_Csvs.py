from dotenv import load_dotenv
from AisDb.Utilities.Helpers import Helpers
from tqdm import tqdm
import json
import yaml
from functools import reduce
import uuid
import dateutil.parser as parser
import os
import sys
load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
AIS_DATA_PATH = os.getenv("AIS_DATA_PATH")
LOGS_PATH = os.getenv("LOGS_PATH")
AIS_REFORMATCSV_DATA_PATH= os.getenv("AIS_REFORMATCSV_DATA_PATH")
SYS_PATH=os.getenv("SYS_PATH")
sys.path.insert(0, f'{SYS_PATH}')

from AisDb.Models.AddressedSafetyMessage import AddressedSafetyMessage
from AisDb.Models.SubscribeMessage import SubscribeMessage
from AisDb.Models.AidsToNavigationReport import AidsToNavigationReport
from AisDb.Models.BaseStationReport import BaseStationReport
from AisDb.Models.BoundingBox import BoundingBox
from AisDb.Models.DataLinkManagementMessage import DataLinkManagementMessage
from AisDb.Models.FilterMessageTypes import FilterMessageTypes
from AisDb.Models.FilterShipMMSI import FilterShipMMSI
from AisDb.Models.PositionReport import PositionReport
from AisDb.Models.ShipCommonData import ShipCommonData
from AisDb.Models.ShipStaticData import ShipStaticData
from AisDb.Models.StandardClassBPositionReport import StandardClassBPositionReport
from AisDb.Models.StaticDataReport import StaticDataReport
from pandas import json_normalize
import pandas as pd
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from glob import glob
import pickle
import pandas as pd
import threading
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
import warnings
warnings.simplefilter(action='ignore')


mapping=Helpers.getNameMapping()
val=Helpers.getValuesStructure()

today = datetime.now().strftime("%Y-%m-%d")
save_direrctory=f"dataCSV_reformated_{today}"

model_classes={
    "AddressedSafetyMessage":AddressedSafetyMessage,
    "AidsToNavigationReport":AidsToNavigationReport,
    "BaseStationReport":BaseStationReport,
    "BoundingBox":BoundingBox,
    "DataLinkManagementMessage":DataLinkManagementMessage,
    "FilterMessageTypes":FilterMessageTypes,
    "FilterShipMMSI":FilterShipMMSI,
    "PositionReport":PositionReport,
    "ShipCommonData":ShipCommonData,
    "ShipStaticData":ShipStaticData,
    "StandardClassBPositionReport":StandardClassBPositionReport,
    "StaticDataReport":StaticDataReport,
    "SubscribeMessage":SubscribeMessage,
}


@staticmethod
def generate_hash(dt, ValuesStructure):
    """
    Generates a hash value for the given data dictionary (`dt`).

    Parameters:
        - dt (dict): The data dictionary for which a hash value is to be generated.

    Returns:
        - str: The hash value for the given data dictionary.
    """
    
    
    
    values=tuple(reduce(lambda d, key: d.get(key) if d else None, key.split("."), dt) 
            for key in ValuesStructure["DataLinkManagementMessage"]["HashVariables"])

    values=[str(i) for i in values]

    st="".join(list(values))
    
def insertFromDF_data(df, key,mapping):

    df.rename(columns={"MetaData.time_utc": "TimeUtc"}, inplace=True)
    df.loc[:, 'SubscribeMessageID'] = None
    df["Geom"] = [f"POINT({row['MetaData.longitude']} {row['MetaData.latitude']})" for _, row in df.iterrows()]
    df["TimeUtc"] = pd.to_datetime(df["TimeUtc"], format="%Y-%m-%d %H:%M:%S.%f %z UTC")
    cols_db = model_classes[key].__table__.columns.keys()[1:]
    df = df.rename(columns=mapping[key + "_mapping"])
    df = df[cols_db]
    directory_path = os.path.join(".", save_direrctory, key)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"{df['TimeUtc'].min().timestamp()}_{df['TimeUtc'].max().timestamp()}.csv")
    df.to_csv(file_path, index=False)
    return {key:file_path}

def insertFromDF_dataLinkManagementMessage(df, key, val, mapping):
    df['MetaData.time_utc'] = pd.to_datetime(df['MetaData.time_utc'], format="%Y-%m-%d %H:%M:%S.%f %z UTC")
    df['data_hash'] = df.apply(lambda x: generate_hash(x.to_dict(), ValuesStructure=val), axis=1)
    df = df.drop_duplicates(subset=['data_hash'])
    df["Geom"] = df.apply(lambda row: "POINT({} {})".format(row["MetaData.longitude".format(key)], row["MetaData.latitude".format(key)]), axis=1)
    df.loc[:, 'SubscribeMessageID'] = None
    df.rename(columns=mapping['DataLinkManagementMessage_mapping'], inplace=True)
    directory_path = os.path.join(".", save_direrctory, key)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"{df['TimeUtc'].min().timestamp()}_{df['TimeUtc'].max().timestamp()}.csv")
    df.to_csv(file_path, index=False)
    return {key:file_path}

def insertFromDF_common_data(df, key, mapping):

    df = df.rename(columns={"MetaData.time_utc": "TimeUtc"})
    df["TimeUtc"] = pd.to_datetime(df["TimeUtc"], format="%Y-%m-%d %H:%M:%S.%f %z UTC")
    if f"Message.{key}.Latitude" in df.columns:
        df["Geom"] = df.apply(lambda row: "POINT({} {})".format(row["Message.{}.Longitude".format(key)], row["Message.{}.Latitude".format(key)]), axis=1)
    else:
        df["Geom"] = df.apply(lambda row: "POINT({} {})".format(row["MetaData.longitude".format(key)], row["MetaData.latitude".format(key)]), axis=1)

    df = df.assign(ShipCommonDataID=[uuid.uuid4() for _ in range(len(df))])
    df = df.rename(columns=mapping[key + "_mapping"])
    df["RepeatIndicator"] = df["RepeatIndicator"].astype(int)
    directory_path = os.path.join(".", save_direrctory, key)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"{df['TimeUtc'].min().timestamp()}_{df['TimeUtc'].max().timestamp()}.csv")
    df.to_csv(
        file_path,
        index=False,
    )
    return {key:file_path}

def reformatCsv(df,key):
    paths=[]

    if key == "Other": 
        path={key:None}
        
    elif key == "SubscribeMessage": 
        path={key:None}
        
    elif key =="DataLinkManagementMessage":
        path = insertFromDF_dataLinkManagementMessage(df,key=key,val=val,mapping=mapping)
    elif key in Helpers.common_types:    
        path = insertFromDF_common_data(df,key,mapping)
    else:
        path = insertFromDF_data(df,key,mapping)
    return path

def reformatBatch(key):

    gl=glob(f"{AIS_REFORMATCSV_DATA_PATH}/{key}/*.csv")
    key=key[:-1]
    for g in gl:
        
        df=pd.read_csv(g,index_col="Unnamed: 0")
        if len(df)>0:
            reformatCsv(df,key)

if __name__ == "__main__":
    gl=glob(f"{AIS_REFORMATCSV_DATA_PATH}/*")
    keys=[g.replace("\\","/").split("/")[-1] for g in gl]

    with Pool(cpu_count()) as p:
        p.map(reformatBatch,keys)



