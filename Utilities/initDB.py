
from glob import glob
import pandas as pd
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
from sqlalchemy.dialects.postgresql import insert
from pandas import json_normalize
from tqdm import tqdm
from sqlalchemy.orm import sessionmaker
import json
from functools import partial
from dotenv import load_dotenv
import os
from insertCsvToDb import getEngine
def initDB():
    load_dotenv()
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    print(f"This script will delete all tables in the database {DATABASE_NAME} hosted on {DATABASE_HOST} and recreate them.")
    ye=input("Press do wish to continue...(Y/n)")
    if ye!="Y":

        db_name,engine=getEngine(db_name=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASSWORD,host=DATABASE_HOST,port=DATABASE_PORT)
        Session = sessionmaker(bind=engine)()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    else:
        pass