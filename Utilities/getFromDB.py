

from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker
from insertCsvToDb import getEngine
from AisDb.Models.ShipCommonData import ShipCommonData
from AisDb.Models.PositionReport import PositionReport
from AisDb.Models.StaticDataReport import StaticDataReport
from AisDb.Models.StandardClassBPositionReport import StandardClassBPositionReport
from AisDb.Models.ShipStaticData import ShipStaticData
from geoalchemy2 import Geometry, WKTElement
import sqlalchemy
from sqlalchemy import literal_column
from tqdm import tqdm
import os

ports_polygon ={
        "Antwerp":[[[4.299317,51.183419],[4.364549,51.169216],[4.509433,51.256513],[4.416734,51.306323],[4.3182,51.384149],[4.270019,51.430824],[4.333306,51.491915],[4.290733,51.556837],[3.484485,51.609358],[3.404833,51.871212],[2.630288,51.728571],[2.446265,51.249836],[3.292222,51.333978],[3.775626,51.323683],[4.160152,51.30652],[4.299317,51.183419]]],
        "singapore":[[[103.016518,1.751264],[103.417053,1.418908],[103.711411,1.490506],[103.994293,1.584111],[104.455744,1.710094],[104.617794,2.182121],[104.888764,2.296892],[105.025635,2.275389],[105.070985,2.171145],[104.917145,1.491216],[103.660141,0.971188],[102.992714,1.402206],[102.811438,1.630039],[103.016518,1.751264]]],
        "Busan":[[[129.238938,35.20188],[128.98213,35.153063],[128.867459,35.141837],[128.83862,35.057589],[128.809094,34.963129],[129.096801,34.972693],[129.295358,34.99894],[129.299478,35.191034],[129.238938,35.20188]]],
        "Los Angeles":[[[-118.157783,33.782564],[-118.311593,33.785417],[-118.322294,33.664564],[-118.074927,33.639897],[-118.057074,33.721443],[-118.157783,33.782564]]],
            
        "Livorno":[[[10.298316,43.620611],[10.120473,43.528105],[10.125279,43.395565],[10.450066,43.383592],[10.351188,43.567413],[10.298316,43.620611]]],
        "Ambarli":[[[28.83202,41.068643],[28.639757,41.062432],[28.549119,40.875831],[28.693316,40.752177],[28.932272,40.688702],[29.108055,40.823903],[29.086082,41.096585],[28.83202,41.068643]]],
        "southampton":[[[-1.216386,50.876412],[-1.421695,50.966424],[-1.570699,50.897633],[-1.370196,50.798811],[-1.306223,50.759962],[-1.15104,50.721298],[-1.070014,50.689126],[-1.137993,50.573007],[-0.667854,50.588491],[-0.722786,50.736443],[-1.192915,50.81169],[-1.216386,50.876412]]],
        "Gdańsk":[[[18.588412,54.381578],[18.81615,54.335391],[19.078222,54.446176],[19.090353,54.57895],[18.521117,54.577491],[18.588412,54.381578]]],

        "Algeciras":[[[-5.266804,36.248734],[-5.604637,36.152345],[-5.662316,35.868029],[-5.316696,35.875716],[-5.080034,35.773401],[-4.579235,35.93976],[-4.785231,36.309055],[-5.266804,36.248734]]],
        "limassol":[[[33.325317,34.736468],[33.137169,34.72214],[32.965511,34.676648],[32.999157,34.622434],[33.002815,34.590637],[33.032803,34.568184],[33.240853,34.471964],[33.418016,34.589662],[33.325317,34.736468]]],
        "Aukland":[[[174.70808,-36.811174],[174.681129,-36.873391],[174.758893,-36.853894],[174.825155,-36.878883],[174.880745,-36.828187],[174.773456,-36.794729],[174.70808,-36.811174]]],
        "cape town":[[[18.392952,-33.559715],[18.524789,-33.901125],[18.252639,-34.015281],[18.071598,-33.658052],[18.241202,-33.494667],[18.392952,-33.559715]]],

    }
def main():
    db_name,engine=getEngine(db_name="aisdata",user="postgres",password="?aisdata?12DB",host="192.168.3.7",port="5432")
    Session = sessionmaker(bind=engine)()

    for port in ports_polygon.keys():
        if port=="Antwerp":
            continue
        polygon_wkt=f"POLYGON(({','.join([f'{p[0]} {p[1]}' for p in ports_polygon[port][0]])}))"
        print("Port of:",port)
        polygon = WKTElement(polygon_wkt, srid=4326)
        
        rounded_time = (func.date_trunc('hour', ShipCommonData.TimeUtc) + 
                text("INTERVAL '1 minute'") * 
                func.round(func.date_part('minute', ShipCommonData.TimeUtc) / 30) * 30
                ).label('rounded_time')


        # Query to select distinct MMSI and the last record based on the rounded time
        q = Session.query(
            ShipCommonData.MMSI,
            func.max(ShipCommonData.TimeUtc).label('last_time')
        ).filter(
            func.ST_Within(ShipCommonData.Geom, polygon)
        ).group_by(
            ShipCommonData.MMSI,
            rounded_time
        ).yield_per(1000)
        for ship in q:
            print(ship)
            

def test():
    from sqlalchemy.orm import aliased
    from sqlalchemy import func,and_,select
    import pandas as pd
    

    db_name,engine=getEngine(db_name="aisdata",user="postgres",password="?aisdata?12DB",host="192.168.3.7",port="5432")
    Session = sessionmaker(bind=engine)()
    for key in ports_polygon.keys():
        if key=="limassol": continue
        if key=="Antwerp": continue
        print("Port of:",key)
        flat_list = [tuple(coords) for sublist in ports_polygon[key] for coords in sublist]
        polygon_string = "("+", ".join(f"{lon} {lat}" for lon, lat in flat_list)+")"
      
        polygon_string=f'POLYGON({polygon_string})'

      # df=pd.read_sql(text(query),con=engine)
    # polygon_geom = WKTElement(polygon_string, srid=4326)  # Adjust SRID as needed
    

        
        polygon_geom = WKTElement(polygon_string, srid=4326)  # Adjust SRID as needed

        # Your other query components seem to be correct
        rounded_time = (
            func.round((func.extract('epoch', ShipCommonData.TimeUtc) / 1800)) * 1800
        ).label('RoundedTime')

        # Window function to assign a row number for each partition of MMSI and RoundedTime
        from sqlalchemy import over
        row_number_column = over(func.row_number(), partition_by=[ShipCommonData.MMSI, rounded_time], order_by=ShipCommonData.TimeUtc).label('rn')

        # Subquery to select only the first row of each partition
        filtered_query = Session.query(
        ShipCommonData,
        rounded_time,
        row_number_column
        ).filter(
            ShipCommonData.MMSI != 0,
            func.ST_Within(ShipCommonData.Geom, polygon_geom)
        ).subquery()

        # Main query to select rows where rn = 1
        # Now, select only the rows where rn = 1 from the filtered and numbered subquery
        result = Session.query(filtered_query).filter(filtered_query.c.rn == 1)

        df=pd.DataFrame(columns=ShipCommonData.__table__.columns.keys())
        for row in tqdm(result.yield_per(10000),total=result.count()):
            cols=ShipCommonData.__table__.columns.keys()
            df=pd.concat([df,pd.DataFrame(row._asdict(),columns=cols,index=[0])])
            # break
        print(df.head())
        os.makedirs(f"/ShipCommonData_30min/{key}",exist_ok=True)
        df.to_csv(f"/ShipCommonData_30min/{key}/ShipCommonData_30min.csv",index=False)
  
        break
    exit()
    os.makedirs(f"/ShipCommonData_30min/{key}",exist_ok=True)
    df_ClassB_position_reports=df[df["Message"]=="StandardClassBPositionReport"]
    df_reports=df[df["Message"]=="PositionReport"]
    df_static=df[df["Message"]=="StaticDataReport"]
    df_ship_static=df[df["Message"]=="ShipStaticData"]
      
    df_reports.to_csv(f"/ShipCommonData_30min/{key}/PositionReport_30min.csv",index=False)
    df_ClassB_position_reports.to_csv(f"/ShipCommonData_30min/{key}/StandardClassBPositionReport_30min.csv",index=False)
    df_static.to_csv(f"/ShipCommonData_30min/{key}/StaticDataReport_30min.csv",index=False)
    df_ship_static.to_csv(f"/ShipCommonData_30min/{key}/ShipStaticData_30min.csv",index=False)



    df.to_csv(f"/ShipCommonData_30min/{key}/ShipCommonData_30min.csv",index=False)

    # results = Session.execute(text(query)).fetchall()

    
    # Execute the query and fetch all results

    
        


if __name__ == "__main__":
        
        test()
        # main()