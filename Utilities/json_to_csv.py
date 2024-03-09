
from AisDb.Utilities.Helpers import Helpers
from tqdm import tqdm
import json
import yaml
from functools import reduce
import uuid
import dateutil.parser as parser

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

mapping=Helpers.getNameMapping()
val=Helpers.getValuesStructure()
# gl=glob("C:/Users/CMMI34\OneDrive - CMMI/Data/dataJSON0/*.json")
save_direrctory="dataCSV"
def jsonFileToCsv(filename):
    js=json.load(open(filename))
    jsonToCsv(js)

def jsonToCsv(js):
    paths=[]
    for key in js.keys(): #for each report type 
        if key == "Other": 
            path={key:None}
            continue
        elif key == "SubscribeMessage": 
            path={key:None}
            continue
        elif key =="DataLinkManagementMessage":
            path =jsToCsv_dataLinkManagementMessage(js=js,key=key,val=val,mapping=mapping)
            
        elif key in Helpers.common_types:    
            path = jsToCsv_common_data(js,key,mapping)
            
        else:
            path = jsToCsv_data(js,key,mapping)
        
        paths.append(path)
    return paths
def loadJsonAndInsert_df():
    with mp.Pool() as pool:
        pool.map(jsonFileToCsv, gl)



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

common_types = ["PositionReport", "ShipStaticData","StandardClassBPositionReport","StaticDataReport"]
@staticmethod
def bounding_box_to_polygon(bounding_box):
    """
    Transform a bounding box into a polygon representation with four points.

    Parameters:
    - bounding_box: A list of two points, where each point is a list of latitude and longitude.
    For example: [[[lat1, lon1], [lat2, lon2]]]

    Returns:
    - A list containing four points, where each point is a tuple of (latitude, longitude)
    representing the corners of the polygon.
    """
    # Unpack the top-left and bottom-right points
    (lat1, lon1), (lat2, lon2) = bounding_box[0]

    # Assuming lat1, lon1 is the top-left and lat2, lon2 is the bottom-right
    # Define other two corners of the rectangle
    top_right = (lat1, lon2)
    bottom_left = (lat2, lon1)

    # List the points in counter-clockwise order
    polygon = [
        (lat1, lon1),  # Top-left
        top_right,     # Top-right
        (lat2, lon2),  # Bottom-right
        bottom_left,    # Bottom-left
        (lat1, lon1)   # Back to Top-left
    ]

    return polygon


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
    
    
    return uuid.uuid5(uuid.NAMESPACE_DNS, st).hex


def insert_data_generic(js, key, mapping, data_type):
    # Check if there is any data to process
    if not js.get(key) or len(js[key]) < 1:
        return
    
    # Normalize the JSON data into a flat DataFrame
    df = json_normalize(js[key])
    
    # Common DateTime parsing
    df['MetaData.time_utc'] = pd.to_datetime(df['MetaData.time_utc'], format="%Y-%m-%d %H:%M:%S.%f %z UTC")
    df.rename(columns={"MetaData.time_utc": "TimeUtc"}, inplace=True)
    # Generate hash and remove duplicates if it's DataLinkManagementMessage
    if data_type == 'DataLinkManagementMessage':
        df['data_hash'] = df.apply(lambda x: generate_hash(x.to_dict(), ValuesStructure=val), axis=1)
        df = df.drop_duplicates(subset=['data_hash'])
    
    # Generate Geom column based on data_type
    if data_type in ['DataLinkManagementMessage', 'common_data']:
        geom_key = "Message.{}.Longitude".format(key) if data_type == 'common_data' else "MetaData.longitude"
        df["Geom"] = df.apply(lambda row: f"POINT({row[geom_key]} {row['MetaData.latitude']})", axis=1)
    else:
        df["Geom"] = [f"POINT({row['MetaData.longitude']} {row['MetaData.latitude']})" for _, row in df.iterrows()]

    # Specific DataLinkManagementMessage handling
    if data_type == 'DataLinkManagementMessage':
        df['SubscribeMessageID'] = None
        df.rename(columns=mapping['DataLinkManagementMessage_mapping'], inplace=True)
    else:
        df = df.rename(columns=mapping[key + "_mapping"])
        if data_type == 'common_data':
            df["RepeatIndicator"] = df["RepeatIndicator"].astype(int)
            df = df.assign(ShipCommonDataID=[uuid.uuid4() for _ in range(len(df))])

    # Directory and file path setup
    directory_path = os.path.join(".", save_direrctory, key)
    os.makedirs(directory_path, exist_ok=True)
    file_name = f"{df['TimeUtc'].min().timestamp()}_{df['TimeUtc'].max().timestamp()}.csv"
    file_path = os.path.join(directory_path, file_name)
    
    # Write to CSV
    df.to_csv(file_path, index=False)




def jsToCsv_dataLinkManagementMessage(js, key, val, mapping):
    if len(js[key]) < 1:
        return
    df = json_normalize(js[key])
    df['MetaData.time_utc'] = pd.to_datetime(df['MetaData.time_utc'], format="%Y-%m-%d %H:%M:%S.%f %z UTC")
    df['data_hash'] = df.apply(lambda x: generate_hash(x.to_dict(), ValuesStructure=val), axis=1)
    df = df.drop_duplicates(subset=['data_hash'])
    df["Geom"] = df.apply(lambda row: "POINT({} {})".format(row["MetaData.longitude".format(key)], row["MetaData.latitude".format(key)]), axis=1)
    df['SubscribeMessageID'] = None
    df.rename(columns=mapping['DataLinkManagementMessage_mapping'], inplace=True)
    directory_path = os.path.join(".", save_direrctory, key)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"{df['TimeUtc'].min().timestamp()}_{df['TimeUtc'].max().timestamp()}.csv")
    df.to_csv(file_path, index=False)
    return {key:file_path}


def jsToCsv_data(js, key,mapping):
    if not js[key]:
        return {key:None}
    df = json_normalize(js[key])
    df.rename(columns={"MetaData.time_utc": "TimeUtc"}, inplace=True)
    df["SubscribeMessageID"] = None
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
    
def jsToCsv_common_data(js, key, mapping):
    if len(js[key]) < 1:
        return
    df = json_normalize(js[key])
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

if __name__ == "__main__":
    loadJsonAndInsert_df()