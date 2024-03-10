import os
import pandas as pd
import sqlalchemy
import psycopg2
from AisDb.Parsing.Helpers import Helpers
from dotenv import load_dotenv
from AisDb.Models.SPGlobalShipDetails import SPGlobalShipDetails
from glob import glob
from sqlalchemy.orm import sessionmaker
from AisDb.Models import  Base
import numpy as np
import yaml
load_dotenv()
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
SP_GLOBAL_SHIP_DETAILS_DATA_PATH = os.getenv("SP_GLOBAL_SHIP_DETAILS_DATA_PATH")
CONFIG_PATH = os.getenv("CONFIG_PATH")


def insertSPGlobalShipDetailsFromCsvToDB():
    with open(f'{CONFIG_PATH}/SPGlobalShipDetailsNameMapping.yaml', 'r') as f:
        config = yaml.safe_load(f)
    db_name,engine=Helpers.getEngine(db_name=DATABASE_NAME,user=DATABASE_USER,password=DATABASE_PASSWORD,host=DATABASE_HOST,port=DATABASE_PORT)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    print(f"Inserting SP Global Ship Details from {SP_GLOBAL_SHIP_DETAILS_DATA_PATH} to DB")
    cont=input("Continue...(Y/n):")
    if cont!="Y":
        return
    try:
        gl=glob(f"{SP_GLOBAL_SHIP_DETAILS_DATA_PATH}/*.csv")
        for csv_file in gl:
            print(f"Inserting {csv_file}")
            df=pd.read_csv(csv_file,skiprows=1)
            df=df.rename(columns=config)
            df.replace({np.NaN: 0}, inplace=True)
            data=df.to_dict(orient="records")
            session.bulk_insert_mappings(SPGlobalShipDetails,data)
            session.commit()
    except Exception as e:
        print(e)
        return
    


if __name__ == '__main__':

    insertSPGlobalShipDetailsFromCsvToDB()