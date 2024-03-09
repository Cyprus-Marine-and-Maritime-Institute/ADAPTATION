from glob import glob
import pandas as pd
import sys
from dotenv import load_dotenv
import os
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
sys.path.insert(0, f"{SYS_PATH}")


from AisDb.Utilities.Helpers import Helpers
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
from AisDb.Models.BaseStationReport import BaseStationReport
from sqlalchemy.dialects.postgresql import insert
from pandas import json_normalize
from tqdm import tqdm
from sqlalchemy.orm import sessionmaker
import json
from functools import partial


from multiprocessing import Pool, cpu_count

from datetime import datetime

import logging

today = datetime.now().strftime("%Y-%m-%d")

logging.basicConfig(
    filename=f'{LOGS_PATH}/{today}_insertcsv.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # include asctime for timestamps
    level=logging.DEBUG  # This will log both INFO and ERROR messages, as ERROR is a higher level than INFO
)


db_name,engine=Helpers.getEngine(db_name=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASSWORD,host=DATABASE_HOST,port=DATABASE_PORT)
ports=["Antwerp", "Singapore", "Busan", "Los-Angeles", "Livorno", "Ambarli", "Southampton", "Gdansk", "Algeciras", "Limassol", "Auckland", "Cape-town"]

subscribe_message = {
                "APIKey": "1d7b4bbfb3293e466302e01f0deed273bcb0d044",
                # "BoundingBoxes": [[[25.835302, -80.207729], [25.602700, -79.879297]], [[33.772292, -118.356139], [33.673490, -118.095731]] ],
                "BoundingBoxes": [[[-90,-180],[90,180]]], # Limassol Port
                # "FiltersShipMMSI": ["368207620", "367719770", "211476060"],
                # "FilterMessageTypes": ["PositionReport"] 
                "Name": ports
        }


def getLatestTimes(Session,keys):
    from sqlalchemy import text
    query = """
    SELECT "MessageType",MAX("TimeUtc") as "latest" FROM "ShipCommonData" GROUP BY "MessageType"
    """
    dates=[]
    for key in keys:
        query2=f"""
            SELECT MAX("TimeUtc") as "latest" FROM "{key}"
        """
        if not key in Helpers.common_types:
            dates.append({key:Session.execute(text(query2)).fetchall()[0][0]})
    results = Session.execute(text(query)).fetchall()
    dd=[{r[0]:r[1]} for r in results ]
    for i in dd:
        dates.append(i)
    dates={list(i.keys())[0]:list(i.values())[0] for i in dates}    
    return dates
def updateDB():
    import datetime
    mapping=Helpers.getNameMapping()
    val=Helpers.getValuesStructure()
    db_name,engine=Helpers.getEngine(db_name=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASSWORD,host=DATABASE_HOST,port=DATABASE_PORT)
    Session = sessionmaker(bind=engine)()
    gl=glob(f"{AIS_DATA_PATH}/*")
    keys=[g.split("/")[-1] for g in gl]
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    latest_dates=getLatestTimes(Session,keys=keys)
    print("Latest dates: ",latest_dates)
    for i in latest_dates:
        if isinstance(latest_dates[i],datetime.datetime):
            continue
        elif latest_dates[i] is None:
            continue
        else:
            print(latest_dates[i])
            if '.' in latest_dates[i]:
            # Split the string on the dot, to separate microseconds and timezone.
                date_string, us_tz = latest_dates[i].split('.', 1)
                # Take only the first 6 digits of the microseconds part and append the timezone again.
                date_string = f"{date_string}.{us_tz[:6]}{us_tz[9:]}"
                # Now we can use '%z' for the timezone.
                date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f%z')
                latest_dates[i]=date_obj
    print("Latest dates: ",latest_dates)
    portBBoxes = json.load(open("./PortsBoundingBoxes.json"))
    portBBoxes=[portBBoxes[p] for p in ports]
    subscribe_message["BoundingBoxes"]=portBBoxes
    id=uuid.uuid4()
    subscribe_message["SubscribeMessageID"]=id
    Helpers.insertSubscribeMessage(subscribe_message,Session)
    for key in keys:

        if key=="DataLinkManagementMessage": continue
        
        glo=glob(f"{AIS_DATA_PATH}/{key}/*.csv")
        new_glo=[]
        try:
            if latest_dates[key] is not None:
                for g in glo:
                    gg=g.split("/")[-1]
                    gg=gg.split(".")[0]+"_"+gg.split(".")[1].split("_")[1]
                    gg=gg.split("_")
                    time_min=gg[0]
                    time_max=gg[1]
                    print(time_min,time_max)
                    from datetime import timezone


                    time_min=datetime.datetime.fromtimestamp(int(time_min))
                    time_max=datetime.datetime.fromtimestamp(int(time_max))
                    time_min = time_min.replace(tzinfo=timezone.utc)
                    time_max = time_max.replace(tzinfo=timezone.utc)
                    latest_dates[key] = latest_dates[key].replace(tzinfo=timezone.utc)
                    if time_min>latest_dates[key]:
                        new_glo.append(g)
                
                glo=new_glo
        except:
            print("No latest date for: ",key)
            

        print(f"Files to insert{key}: ",len(glo))
        print("Inserting: ",key)

        insert_data_with_fixed_args = partial(Helpers.insert_data,key,id)

        with Pool(cpu_count()) as p:
            p.map(insert_data_with_fixed_args,glo)




def insertFromScratch():
    import datetime
    mapping=Helpers.getNameMapping()
    val=Helpers.getValuesStructure()
    
    Session = sessionmaker(bind=engine)()
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # return
    gl=glob(f"{AIS_DATA_PATH}/*")
    keys=[g.replace("\\","/").split("/")[-1] for g in gl]
    portBBoxes = json.load(open("./PortsBoundingBoxes.json"))
    portBBoxes=[portBBoxes[p] for p in ports]
    subscribe_message["BoundingBoxes"]=portBBoxes
    id=uuid.uuid4()
    subscribe_message["SubscribeMessageID"]=id
    Helpers.insertsubscribemessage(subscribe_message,Session)
    Session.close()
    print("Inserted subscribe message")
    hl=Helpers()
    for key in keys:

        # if key=="DataLinkManagementMessage": continue
        # if key!= "ShipStaticData": continue
        # print(f"Inserting {key}")
        # print(f"Directory {AIS_DATA_PATH}/{key}\n")
        
        glo=glob(f"{AIS_DATA_PATH}/{key}/*.csv")
        # print(f"Files to insert{key}: ",len(glo))
    
        
        insert_data_with_fixed_args = partial(Helpers.insert_data,hl.getSelf(),key,id,None)


        with Pool(processes=5) as p:
            p.map(insert_data_with_fixed_args,glo)


if __name__ == "__main__":
    # pass
    insertFromScratch()
    