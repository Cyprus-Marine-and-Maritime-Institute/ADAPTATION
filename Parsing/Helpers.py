import yaml
from functools import reduce
import uuid
import dateutil.parser as parser
import sys
import os
from .dataClasses import PositionReport, ShipStaticData, StandardClassBPositionReport, StaticDataReport,Dimension, Eta, ReportA, ReportB
from dotenv import load_dotenv
import traceback
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
import sys
sys.path.insert(0, f"{SYS_PATH}")

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
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
import pandas as pd

from sqlalchemy import create_engine

from functools import reduce
import uuid
import dateutil.parser as parser
from datetime import datetime

import logging

today = datetime.now().strftime("%Y-%m-%d")

logging.basicConfig(
    filename=f'{LOGS_PATH}/{today}_insertcsv.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # include asctime for timestamps
    level=logging.DEBUG  # This will log both INFO and ERROR messages, as ERROR is a higher level than INFO
)

class Helpers:

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
    def __init__(self) -> None:
        self.engine=None
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
        # Check if bounding box is polygon or bounding box
        if len(bounding_box[0]) == 2:
                
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
        else:
            polygon=[]
            print(bounding_box)
            for i in bounding_box[0]:
                polygon.append((i[1],i[0]))
            polygon.append((bounding_box[0][0][1],bounding_box[0][0][0]))
            # print ("_______________________",polygon,"_______________________")
            return polygon
        
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


    @staticmethod
    
    def insert_dataLinkManagementMessage(js,engine,key,time_df,val,mapping):

        if len(js[key])<1:
            return
        df=json_normalize(js[key])
        df['MetaData.time_utc']=df['MetaData.time_utc'].apply(lambda x: x.split(" ")[0] +" "+ x.split(" ")[1] +" "+ x.split(" ")[3])
        # get col names
        
        def generate_hash(dt, ValuesStructure):
            values = (str(dt.get(key)) for key in ValuesStructure["DataLinkManagementMessage"]["HashVariables"])
            concatenated_values = "".join(values)
            return uuid.uuid5(uuid.NAMESPACE_DNS, concatenated_values).hex

        df['data_hash']=df.apply(lambda x: generate_hash(x.to_dict(),ValuesStructure=val),axis=1)
        df=df.drop_duplicates(subset=['data_hash'])
        df.rename(columns=mapping['DataLinkManagementMessage_mapping'],inplace=True)
        df['TimeUtc']=pd.to_datetime(df['TimeUtc'])
        
        # min_time=df['TimeUtc'].min().timestamp()
        # max_inserted=time_df[time_df["Unnamed: 0"]==key]["latest"].values[0]
        # # print(f"{key}",max_inserted)
        # if float(min_time)<float(max_inserted):
        #     print(f"{min_time}<{max_inserted}")
        #     print(f"Data for {key} already inserted")
        #     return


        df=df.sort_values(by=['TimeUtc'])
        df['Geom']=df.apply(lambda x: f"POINT({x['longitude']} {x['latitude']})",axis=1)
        df['subscribemessageID']=None
        # print(len(df))
        def insert_on_duplicate(table, conn, keys, data_iter):


            table=table.table
            
            items= list(data_iter)
            
            data_dicts = [dict(zip(keys, item)) for item in items]

            insert_stmt=insert(table).values(data_dicts)
            
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['data_hash'])

            conn.execute(do_nothing_stmt)
            
        directory_path = f"./dataCSV/{key}"
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
        df.to_csv(f"./dataCSV/{key}/{df['TimeUtc'].min().timestamp()}.csv",index=False)
        df=df[DataLinkManagementMessage.__table__.columns.keys()[1:]]
        df.to_sql("DataLinkManagementMessage",con=engine,if_exists='append',index=False,method=insert_on_duplicate)
        
    @staticmethod
    def insert_data_js(js,engine,key,time_df,mapping):
        

        if len(js[key])<1:
            return
        df=json_normalize(js[key])

        # print(df.columns)
        df['MetaData.time_utc']=df['MetaData.time_utc'].apply(lambda x: x.split(" ")[0] +" "+ x.split(" ")[1] +" "+ x.split(" ")[3])
        df.rename(columns={"MetaData.time_utc":"TimeUtc"},inplace=True)
        df['subscribemessageID']=None
        df['Geom']=df.apply(lambda x: f"POINT({x[f'MetaData.longitude']} {x[f'MetaData.latitude']})",axis=1)
        df['TimeUtc']=pd.to_datetime(df['TimeUtc'])

        cols=df.columns
        cols_db= Helpers.model_classes[key].__table__.columns.keys()

        mapping_=mapping[key+"_mapping"]
        df.rename(columns=mapping_,inplace=True)

        directory_path = f"./dataCSV/{key}"
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
        df.to_csv(f"./dataCSV/{key}/{df['TimeUtc'].min().timestamp()}.csv",index=False)

        cols_db=cols_db[1:]
        df=df[cols_db]
        df.to_sql(key,con=engine,if_exists='append',index=False)
        

    def insert_common_data(js,engine,key,time_df,mapping):

        # print("Insert Data: ",key)

        if len(js[key])<1:
            return
        df=json_normalize(js[key])

        cols=df.columns
        cols_db= Helpers.model_classes[key].__table__.columns.keys()
        cols_common=Helpers.model_classes["ShipCommonData"].__table__.columns.keys()
        # print(cols)
        # print(cols_db)
        # print(cols_common)
        
        df['MetaData.time_utc']=df['MetaData.time_utc'].apply(lambda x: x.split(" ")[0] +" "+ x.split(" ")[1] +" "+ x.split(" ")[3])
        df.rename(columns={"MetaData.time_utc":"TimeUtc"},inplace=True)
        df['subscribemessageID']=None
        if f"Message.{key}.Latitude" in df.columns:
            df['Geom']=df.apply(lambda x: f"POINT({x[f'Message.{key}.Longitude']} {x[f'Message.{key}.Latitude']})",axis=1)
        else:
            df['Geom']=df.apply(lambda x: f"POINT({x[f'MetaData.longitude']} {x[f'MetaData.latitude']})",axis=1)
        df['TimeUtc']=pd.to_datetime(df['TimeUtc'])
        # get col names
        # min_time=df['TimeUtc'].min().timestamp()
        # max_inserted=time_df[time_df["Unnamed: 0"]==key]["latest"].values[0]
        # # print(f"{key}",max_inserted)
        # if float(min_time)<float(max_inserted):
        #     print(f"{min_time}<{max_inserted}")
        #     print(f"Data for {key} already inserted")
        #     return

        # print(mapping)
        mapping_=mapping[key+'_mapping']
        df['ShipCommonDataID'] = [uuid.uuid4() for _ in range(len(df))]
        
            
        
        df.rename(columns=mapping_,inplace=True)
        # print(df.columns)
        
        df['RepeatIndicator'] = df['RepeatIndicator'].astype(int)

        directory_path = f"./dataCSV/{key}"
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)

        df.to_csv(f"./dataCSV/{key}/{df['TimeUtc'].min().timestamp()}.csv",index=False)
        ShipCommonData_df=df[cols_common]
        cols_db=cols_db[1:]
        other_df=df[cols_db]

        ShipCommonData_df.to_sql("ShipCommonData",con=engine,if_exists='append',index=False)
        other_df.to_sql(key,con=engine,if_exists='append',index=False)
    @staticmethod
    def insertsubscribemessage(subscribe_message,session):
        # id=uuid.uuid4()
        print(subscribe_message)
        obj={
            "SubscribeMessageID":subscribe_message["SubscribeMessageID"],
            "APIKey":subscribe_message["APIKey"],
            "Name":",".join(subscribe_message["Name"]),
        }
        subscribemessage_=SubscribeMessage(**obj)
        session.add(subscribemessage_)
        session.commit()
        if "BoundingBoxes" in subscribe_message:
            for i in subscribe_message["BoundingBoxes"]:
                print(i)
                poly=Helpers.bounding_box_to_polygon([i])

                obj={
                    "SubscribeMessageID":id,
                    "Polygon":f"POLYGON(({', '.join([' '.join(map(str, p)) for p in poly])}))"
                }
                BoundingBox_=BoundingBox(**obj)
                session.add(BoundingBox_)
        mmsi_list=[]
        if "FiltersShipMMSI" in subscribe_message:
            for i in subscribe_message["FiltersShipMMSI"]:
                mmsi_list.append(i)
            obj={
                "SubscribeMessageID":id,
                "MMSI":",".join(mmsi_list)
            }
            FilterShipMMSI_=FilterShipMMSI(**obj)
            session.add(FilterShipMMSI_)
        message_type_list=[]
        if "FilterMessageTypes" in subscribe_message:
            for i in subscribe_message["FilterMessageTypes"]:
                ",".join(message_type_list)
            
            obj={
                "SubscribeMessageID":id,
                "MessageType":",".join(message_type_list)
            }
            FilterMessageTypes_=FilterMessageTypes(**obj)
            session.add(FilterMessageTypes_)
            session.commit()

    @staticmethod
    def getEngine(db_name,user,password,host,port):
            DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
            engine = create_engine(DATABASE_URI, echo=False)  # echo=True will print SQL statements.
            return db_name,engine

    @staticmethod
    def getValuesStructure():
            """
            Loads a structure for values from a YAML file, storing the result in the `ValuesStructure` attribute of the class.
            
            Side Effects:
                - Sets the `ValuesStructure` attribute with the loaded structure from the YAML file.
            
            Notes:
                - Expects the YAML file to be located at "./JSONStructure.yaml".
                - If there's an error loading the YAML, an exception will be printed and an empty tuple will be returned.
            """
            with open("./config/JSONStructure.yaml", "r") as f:
                try:
                    return yaml.safe_load(f)
                except yaml.YAMLError as exc:
                    print(exc)
                    return ()
    def getNameMapping():
                        
            with open("./config/NameMappings.yaml", "r") as f:
                try:
                    return yaml.safe_load(f)
                except yaml.YAMLError as exc:
                    print(exc)
                    return ()
    
    def getSelf(self):
        return self
    def insert_data(self,key,id,engine_=None,g=None):

        if g is None:
            print("No file: ",key)
            return
        if engine_ is not None:
            Session = sessionmaker(bind=engine_)()
            engine=engine_
        else:
            if self.engine==None:
                db_name,engine=Helpers.getEngine(db_name=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASSWORD,host=DATABASE_HOST,port=DATABASE_PORT)
                self.engine=engine
            engine=self.engine
            Session = sessionmaker(bind=engine)()
        df=pd.read_csv(g)
        if df.empty:
            print("Empty: ",key)
            return 0
        cols=Helpers.model_classes[key].__table__.columns.keys()
        df["SubscribeMessageID"]=id
        df_=df[cols[1:]]
        # print(f"Inserting: {len(df_)} {key}")
        df_=df_.replace({pd.NaT: None})
        
        # print(df_.head())

        timestamp = datetime.now().strftime("%Y-%m-%d")
        if key== "PositionReport":
            # check if valid
            position_report_instances = [
                PositionReport(**row.to_dict())
                for _, row in df.iterrows()
            ]
            valid=[i.is_valid() for i in position_report_instances]
            if False in valid:
                df.to_csv(f"{LOGS_PATH}/failed_inserts_{key}_{today}_{timestamp}.csv",index=False)
            return 0

        elif key=="ShipStaticData":
            # check if valid

            ship_static_data_instances = [
                ShipStaticData(
                    **{k: v for k, v in row.to_dict().items() if k not in ['A', 'B', 'C', 'D', 'Day', 'Hour', 'Minute', 'Month']},
                    Dimension=Dimension(A=row['A'], B=row['B'], C=row['C'], D=row['D']),
                    Eta=Eta(Day=row['Day'], Hour=row['Hour'], Minute=row['Minute'], Month=row['Month'])
                )
                for i, row in df_.iterrows()
            ]

            valid=[i.is_valid() for i in ship_static_data_instances]
            if False in valid:
                # write the df to file failed

                df.to_csv(f"{LOGS_PATH}/failed_inserts_{key}_{today}_{timestamp}.csv",index=False)
                return 0
        elif key== "StandardClassBPositionReport":
            standard_class_B_position_report = [
                StandardClassBPositionReport(**row.to_dict())
                for _, row in df.iterrows()
            ]


            valid=[i.is_valid() for i in standard_class_B_position_report]
            if False in valid:
                # write the df to file failed
                df.to_csv(f"{LOGS_PATH}/failed_inserts_{key}_{today}_{timestamp}.csv",index=False)
                return 0


        elif key=="StaticDataReport":
            static_data_reports = []
            for _, row in df.iterrows():
                report_a = ReportA(Name=row['Name'], Valid=row['Valid']) if 'Name' in row else None
                report_b = None
                if 'CallSign' in row and 'A' in row and 'B' in row and 'C' in row and 'D' in row:
                    dimension = Dimension(A=row['A'], B=row['B'], C=row['C'], D=row['D'])
                    report_b = ReportB(
                        CallSign=row['CallSign'],
                        Dimension=dimension,
                        FixType=row['FixType'],
                        ShipType=row['ShipType'],
                        Spare=row['Spare'],
                        VenderIDModel=row['VenderIDModel'],
                        VenderIDSerial=row['VenderIDSerial'],
                        VendorIDName=row['VendorIDName'],
                        Valid=row['Valid']
                    )
                static_data_report = StaticDataReport(
                    MessageID=row['MessageID'],
                    PartNumber=row['PartNumber'],
                    RepeatIndicator=row['RepeatIndicator'],
                    ReportA=report_a,
                    ReportB=report_b,
                    Reserved=row['Reserved'],
                    UserID=row['UserID'],
                    Valid=row['Valid']
                )
                static_data_reports.append(static_data_report)

            valid=[i.is_valid() for i in static_data_reports]
            if False in valid:
                # write the df to file failed
                df.to_csv(f"{LOGS_PATH}/failed_inserts_{key}_{today}_{timestamp}.csv",index=False)
                return 0
        try:
            if key in Helpers.common_types:
                try:
                    cols_com=ShipCommonData.__table__.columns.keys()
                    df_com=df[cols_com]
                    df_com.to_sql("ShipCommonData".lower(),con=engine,if_exists='append',index=False)
                    df_.to_sql(key.lower(),con=engine,if_exists='append',index=False)
                    # print("Inserted: ",key)
                except Exception as e:
                    today = datetime.now().strftime("%Y-%m-%d")
                    logging.error(f"Failed to insert: {key} : {g}", exc_info=True)
                    log_file=open(f"{LOGS_PATH}/failed_inserts_{today}.txt","a")
                    log_file.write(f"Failed to insert: {key} : {g}\n")
                    f.write(f"Error: {traceback.format_exc()}\n")
                    print(f"Failed to insert: {key} : {g}")
                    
            elif key=="DataLinkManagementMessage":
                # for i in range(len(df_)):
                try:
                    df_.to_sql(key.lower(),con=engine,if_exists='append',index=False)
                    # df_.iloc[i:i+1].to_sql(key,con=engine,if_exists='append',index=False)
                    # print("Inserted: ",df_.iloc[i:i+1])
                    # print("Inserted: ",key)
                except Exception as e:
                    today = datetime.now().strftime("%Y-%m-%d")
                    logging.error(f"Failed to insert: {key} : {g}", exc_info=True)
                    with open(f"{LOGS_PATH}/failed_inserts_{today}.txt","a") as f:
                        f.write(f"Failed to insert: {key} : {g}\n")
                        f.write(f"Error: {traceback.format_exc()}\n")
                    print(f"Failed to insert: {key} : {g}")
                
            else:
                try:
                    df_.to_sql(key.lower(),con=engine,if_exists='append',index=False)
                    # print("Inserted: ",key,flush=True)
                except Exception as e:
                    # print("Error: ",e)
                    today = datetime.now().strftime("%Y-%m-%d")
                    logging.error(f"Failed to insert: {key} : {g}", exc_info=True)
                    with open(f"{LOGS_PATH}/failed_inserts_{today}.txt","a") as f:
                        f.write(f"Failed to insert: {key} : {g}\n")
                        f.write(f"Error: {traceback.format_exc()}\n")
                    print(f"Failed to insert: {key} : {g}",flush=True)

        except Exception as e:
            print('Error: ',e)
            today = datetime.now().strftime("%Y-%m-%d")
            logging.error(f"Failed to insert: {key} : {g}", exc_info=True)
            with open(f"{LOGS_PATH}/failed_inserts_{today}.txt","a") as f:
                f.write(f"Failed to insert: {key} : {g}\n")
            print(f"Failed to insert: {key} : {g}")
        finally:
            Session.close()
            return len(df_)

    
    @staticmethod                
    def extract_value_from_dict(dt, key, report_type):
        key_parts = key.split(".")
        # Replace wildcard with the report_type
        key_parts = [report_type if part == '*' else part for part in key_parts]
            
        return reduce(lambda d, k: d.get(k) if d else None, key_parts, dt)
    @staticmethod                
    def get_values(ReportType, dt, VariableType="DBStoreVariables", i=None,ValuesStructure=None):
        """
        Extracts values from the given data dictionary (`dt`) based on the specified report type 
        and variable type. The method organizes the extracted data into a tuple, which can be used 
        for database insertion or other operations.

        Parameters:
            - ReportType (str): Specifies the type of report.
            - dt (dict): The data dictionary from which values are to be extracted.
            - VariableType (str, optional): Determines the set of variables to extract. Defaults to 'DBStoreVariables'.
            - i (int, optional): An optional index value that can be added to the data.

        Returns:
            - tuple: A tuple containing the extracted values.
        """

        if ValuesStructure is None:
            ValuesStructure = Helpers.getValuesStructure()
        
        dt['ShipCommonDataID']=uuid.uuid4()
        
        if ReportType == "PositionReport" or ReportType== "StandardClassBPositionReport":
            dt['Geom']=f"POINT({dt['Message'][ReportType]['Longitude']} {dt['Message'][ReportType]['Latitude']})"
        else:
            dt['Geom']=f"POINT({dt['MetaData']['longitude']} {dt['MetaData']['latitude']})"
        dt['MetaData']['time_utc']=dt['MetaData']['time_utc'].split(" ")
        dt['MetaData']['time_utc']=" ".join(dt['MetaData']['time_utc'][:2])
        dt['MetaData']['time_utc']=parser.parse(dt['MetaData']['time_utc']).strftime("%Y-%m-%d %H:%M:%S.%f")
        if ReportType == "MetaData" and VariableType != "HashVariables":
            dt["MetaData"]['latitude'] = dt["MetaData"].get('latitude')
            dt["MetaData"]['longitude'] = dt["MetaData"].get('longitude')
            
        if ReportType != "MetaData" and "Latitude" in dt.get("Message", {}).get(ReportType, {}):
            dt["Message"][ReportType]["Latitude"] = dt["Message"][ReportType].get("Latitude")
            dt["Message"][ReportType]["Longitude"] = dt["Message"][ReportType].get("Longitude")

        if ReportType == "DataLinkManagementMessage":
            dt['hash']=Helpers.generate_hash(dt,ValuesStructure=ValuesStructure)

        if i is not None:
            dt['Index'] = i
        if ReportType in Helpers.common_types:
            common_values = tuple(
                Helpers.extract_value_from_dict(dt, key, ReportType)
                for key in ValuesStructure["CommonShipData"]["DBStoreVariables"]
            )
            unique_values = (None,)+tuple(
                reduce(lambda d, key: d.get(key) if d else None, key.split("."), dt) 
                for key in ValuesStructure[ReportType][VariableType]
            )
            return (unique_values,common_values)
        return tuple([(None,)+tuple(
            reduce(lambda d, key: d.get(key) if d else None, key.split("."), dt)
            for key in ValuesStructure[ReportType][VariableType]
            ),None])
    
    