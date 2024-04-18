# !~/miniconda3/envs/aisenv/bin/python
import sys
sys.path.append('./')
import asyncio
import websockets
import json
import threading
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime
import os
import traceback
from dotenv import load_dotenv
import os
from functools import reduce
from sqlalchemy import create_engine
import uuid
from glob import glob
from sqlalchemy.orm import sessionmaker
import logging
import pandas as pd
from pandas import json_normalize
import yaml
from uuid import UUID
save_direrctory="/data/dataToInsert/dataCSV"
json_save_direrctory="/data/dataToInsert/dataJSON"
common_types = ["PositionReport", "ShipStaticData","StandardClassBPositionReport","StaticDataReport"]


with open("./config/NameMappings.yaml") as f:
    mapping=yaml.safe_load(f)
with open("./config/JSONStructure.yaml") as f:
    val=yaml.safe_load(f)

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

def jsonFileToCsv(filename):
    js=json.load(open(filename))
    jsonToCsv(js)
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
    df = df.rename(columns=mapping[key + "_mapping"])
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
            
        elif key in common_types:    
            path = jsToCsv_common_data(js,key,mapping)
            
        else:
            path = jsToCsv_data(js,key,mapping)
        
        paths.append(path)
    return paths

# Configure the logging system
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(dotenv_path)
print(os.getcwd())
def clear_environment_variables():
    keys = list(os.environ.keys())
    for key in keys:
        del os.environ[key]

# Clear existing environment variables
clear_environment_variables()
load_dotenv(dotenv_path=dotenv_path)
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
LOGS_PATH=os.getenv("LOGS_PATH")
today=datetime.now().strftime("%Y-%m-%d")
import logging
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
if not LOGS_PATH:
    LOGS_PATH = "/data/ais_collection/logs"
# Now your makedirs call

# os.makedirs(LOGS_PATH, exist_ok=True)



class AISstream():
    """Handles streaming of AIS data, processes the streamed data, and saves it to a database.
        Attributes:
            - subscribe_message: The message data to subscribe with.
            - dbHandler: Database handler object for database operations.
            - temp_data: Temporary storage for the streamed data.
            - temp_data_index: Index to keep track of the current position in temp_data.
            - savingtoDB: Flag to check if data is currently being saved to the database.
            - subscribe_message_id: ID of the subscribe message.
            - sizeExceed: Flag to check if the size of the streamed data exceeds a certain limit.
            - DBlock: Lock object to ensure thread-safety during database operations.
            - sumLock: Lock object to ensure thread-safety when summing data.
            - sem: Semaphore object to control concurrent access.
            - executor: Thread pool executor for concurrent tasks.
        """
    def __init__(self, subscribe_message,checkPoint=50):
        """
        Initialize the AISstream class.

        Parameters:
            - subscribe_message (dict): The message data to subscribe with.
            - dbHandler: Database handler object for database operations.
        """
        self.subscribe_message = subscribe_message
        self.temp_data = [self._initialize_data_dict()]*50
        self.temp_data_index = 0
        self.subscribe_message_id = uuid.uuid4()
        self.subscribe_message["SubscribeMessageID"]=self.subscribe_message_id
        self.sizeExceed = False
        self.checkPoint=checkPoint
        self.DBlock = threading.Lock()  # To prevent race conditions
        self.sumLock = threading.Lock()
        self.sem=threading.Semaphore(1)
        self.executor = ThreadPoolExecutor(max_workers=5)  # Adjust as needed
        self.retry_time=0
        logging.info("AISstream object created")
        

    @staticmethod
    def _initialize_data_dict():
        """
        Initialize the data dictionary for temporary storage of streamed data.

        Returns:
            - dict: Initialized data dictionary.
        """
        return {
            "PositionReport": [],
            "StaticDataReport": [],
            "DataLinkManagementMessage": [],
            "StandardClassBPositionReport": [],
            "ShipStaticData": [],
            "BaseStationReport": [],
            "AidsToNavigationReport": [],
            "AddressedSafetyMessage": [],
            "Other": []
        }

    def connect(self):
        """
        Initiate the connection process for AIS data streaming.
        """
        logging.info("Connecting to AISstream")
        asyncio.run(self.connect_async())

    async def connect_async(self):
        """
        Asynchronous method to establish connection and handle incoming AIS data stream.
        """

        total=tqdm(range(self.checkPoint))
        while True:
            try:
                async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
                    if "APIKey" in self.subscribe_message and "BoundingBoxes" in self.subscribe_message:
                        copyofsub={
                            "APIKey": self.subscribe_message["APIKey"],
                            "BoundingBoxes": self.subscribe_message["BoundingBoxes"],
                        }
                    else:
                        copyofsub={
                            "APIKey": "key",
                            "BoundingBoxes": "bg"
                        }
                        
                    print("Sending subscribe message")
                    self.subscribe_message_json = json.dumps(copyofsub)
                    await websocket.send(self.subscribe_message_json)

                    async for message_json in websocket:
                        message = json.loads(message_json)
                       
                        if "MessageType" not in message:
                            print(message)
                            continue
                        message_type = message["MessageType"]
                        if message_type in self.temp_data[self.temp_data_index].keys():
                            self.temp_data[self.temp_data_index][message_type].append(message)


                        self.sem.acquire()
                        totalSize = sum(len(self.temp_data[self.temp_data_index][key]) for key in self.temp_data[self.temp_data_index].keys())
                        additional_size=totalSize-total.n
                        total.update(additional_size)
                        if totalSize > self.checkPoint:
                                total=tqdm(range(self.checkPoint))
                                threading.Thread(target=self.save_to_db, args=(self.temp_data[self.temp_data_index],self.temp_data_index,self.subscribe_message_id)).start()
                                self.temp_data_index = (self.temp_data_index + 1) % 49
                                self.temp_data[self.temp_data_index] = self._initialize_data_dict()
                                
                        self.sem.release()
                        
            except (websockets.exceptions.ConnectionClosedError, asyncio.exceptions.CancelledError):
                print("Connection lost. Reconnecting...")
                logging.error("Connection lost. Reconnecting...", exc_info=True)
                await asyncio.sleep(2)  # Reconnection wait time
                
            except Exception as e:
                trace=traceback.format_exc()
                with open("UknownConnectionErrors.txt","a+") as f:
                    f.write(str({"Error":str(e),"StackTrace":trace,"Time":datetime.now().timestamp(),"Data":message}))

                
                logging.error("Error: %s", e, exc_info=True)
                

                await asyncio.sleep(2)

    def checkSize(self, messages):
        """
        Check the total size of the given messages.

        Parameters:
            - messages (dict): Dictionary containing AIS data.

        Returns:
            - int: Total size of the messages.
        """
        totalSize = sum(len(messages[key]) for key in messages.keys())
        return totalSize
        print(totalSize)

    def uuid_encoder(self,obj):
        if isinstance(obj, UUID):
            return str(obj)
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


    def clearArr(self,index):
        """
        Clear the data array for the given index.

        Parameters:
            - index (int): Index of the array to be cleared.
        """
        # print("Clearing: "+str(index)+"\n")
        for key in self.temp_data[index].keys():
            self.temp_data[index][key].clear()

    def save_to_db(self, messages,temp_data_index,subscribe_message_id):
            """
            Save the given messages to the database and dump them to a JSON file.

            Parameters:
                - messages (dict): Dictionary containing AIS data.
                - temp_data_index (int): Index of the temp_data where the messages are stored.
                - subscribe_message_id (int): ID of the subscribe message.
            """
            messages["SubscribeMessage"]=self.subscribe_message
            logging.info("Saving to DB")
            time_now = datetime.now().timestamp()
            os.makedirs(json_save_direrctory,exist_ok=True)
            try:
                with open (json_save_direrctory+"/data_"+str(time_now)+".json", 'w') as file:
                    json.dump(messages, file, default=self.uuid_encoder)
                logging.info("Dumped to JSON: %s", "data_"+str(time_now)+".json")
            except Exception as e:
                logging.error("Error at dumping to json", exc_info=True)
            file_paths=jsonToCsv(messages)
            
            self.clearArr(temp_data_index)


if __name__ == "__main__":
    # print("Current User",os.getlogin())
    os.makedirs(save_direrctory, exist_ok=True)
    os.makedirs(json_save_direrctory, exist_ok=True)
    os.makedirs(LOGS_PATH, exist_ok=True)
    os.makedirs(LOGS_PATH, exist_ok=True)
    with open('/home/charalambos/Documents/ADAPTATION/Collector/ADAPTATION/testttt.txt', 'w') as f:
        f.write("test")
        
    # list the files in the save directory
    logging.basicConfig(
    filename=f'{LOGS_PATH}/{today}_stream.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # include asctime for timestamps
    level=logging.INFO  # This will log both INFO and ERROR messages, as ERROR is a higher level than INFO
)
    f=open("./PortsBoundingBoxes.json")
    ports_cords=json.load(f)
    f.close()
    try:
        index = os.sys.argv.index("--ports")+1
        ports=[]
        port_names=[]

        while index < len(os.sys.argv) and not os.sys.argv[index].startswith("--"):
            try:
                ports.append(ports_cords[os.sys.argv[index]])
                port_names.append(os.sys.argv[index])
            except:
                print("Port not found: "+os.sys.argv[index])
                exit()
            index += 1

        print(ports)
    except:
        ports=[port for port in ports_cords.values()]
        port_names=[port for port in ports_cords.keys()]
    api_key = os.getenv("API_KEY")
    print(api_key)
    subscribe_message = {
            "APIKey": api_key,
            # "BoundingBoxes": [[[25.835302, -80.207729], [25.602700, -79.879297]], [[33.772292, -118.356139], [33.673490, -118.095731]] ],
            "BoundingBoxes": ports, # Limassol Port
            # "FiltersShipMMSI": ["368207620", "367719770", "211476060"],
            # "FilterMessageTypes": ["PositionReport"] 
            "Name": port_names
    }
    print(subscribe_message)
    logging.info("Starting AISstreamConnector")
    logging.info("Subscribing to: "+str(subscribe_message["Name"]))
    AISstream(subscribe_message,5000).connect()
