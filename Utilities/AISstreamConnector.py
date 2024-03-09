
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
from json_to_csv import jsonToCsv
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import uuid
from AisDb.Models import *
from glob import glob
from sqlalchemy.orm import sessionmaker
import logging
from AisDb.Utilities.Helpers import Helpers
import pandas as pd


# Configure the logging system
load_dotenv()
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

logging.basicConfig(
    filename=f'{LOGS_PATH}/{today}_stream.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # include asctime for timestamps
    level=logging.INFO  # This will log both INFO and ERROR messages, as ERROR is a higher level than INFO
)


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
        self.db_name,self.engine=Helpers.getEngine(db_name=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASSWORD,host=DATABASE_HOST,port=DATABASE_PORT)
        print(f"Connected to database: {self.db_name}")
        logging.info(f"Connected to database: {self.db_name}")


        Session = sessionmaker(bind=self.engine)()
        
        Base.metadata.create_all(self.engine)
        Helpers.insertsubscribemessage(self.subscribe_message,Session)
        Session.close()
        
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
                    copyofsub={
                        "APIKey": self.subscribe_message["APIKey"],
                        "BoundingBoxes": self.subscribe_message["BoundingBoxes"],
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
                                threading.Thread(target=self.save_to_db, args=(self.temp_data[self.temp_data_index],self.temp_data_index,self.subscribe_message_id,self.engine)).start()
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

    def save_to_db(self, messages,temp_data_index,subscribe_message_id,engine):
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
            os.makedirs("./dataJSON/data_",exist_ok=True)
            try:
                with open ("./dataJSON/data_"+str(time_now)+".json", 'w') as file:
                    json.dump(messages, file, default=self.uuid_encoder)
                logging.info("Dumped to JSON: %s", "data_"+str(time_now)+".json")
            except Exception as e:
                logging.error("Error at dumping to json", exc_info=True)
            file_paths=jsonToCsv(messages)
            

            # print(file_paths)
            # return
            for p in file_paths:
                if p is not None and isinstance(p, dict):
                    key, value = next(iter(p.items()))  # This safely gets the first key-value pair
                    count1=sessionmaker(bind=engine)().query(Helpers.model_classes[key]).count()
                    # print(f"Count {key}: ",count1)
                    lenth=0
                    if value is not None:
                        value.replace("\\","/")
                        print("Inserting: \n",value)
                        
                        lenth=Helpers.insert_data(key, subscribe_message_id,engine_=engine,g=value)
                        try:
                            pass
                        except Exception as e:
                            logging.error("Error at inserting to db", exc_info=True)
                else:
                    print("Error: The data object 'p' is None or not a dictionary.")

                count=sessionmaker(bind=engine)().query(Helpers.model_classes[key]).count()
                # print(f"Count {key}: ",count)
                print(f"Should have incresed by {lenth} but {key} increased by ",count-count1)
            
            self.clearArr(temp_data_index)


if __name__ == "__main__":
    f=open("./PortsBoundingBoxes.json")
    ports_cords=json.load(f)
    f.close()
    # print(ports_cords)
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
    subscribe_message = {
            "APIKey": "66e9b3986ecfcefc645e9522afea2468d4e1de82",
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
