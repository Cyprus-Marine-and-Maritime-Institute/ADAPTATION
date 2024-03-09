
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
LOGS_PATH=os.getenv("LOGS_PATH")
SYS_PATH=os.getenv("SYS_PATH")
import sys
sys.path.insert(0, f'{SYS_PATH}')

# from AISstreamConnector import AISstream
# from initDB import initDB
# from insertCsvToDb import *
# from json_to_csv import *
# from PopulateResampledTable import *
# from reformat_Csvs import *
# from helpers import *
# from ..Models.AddressedSafetyMessage import AddressedSafetyMessage
