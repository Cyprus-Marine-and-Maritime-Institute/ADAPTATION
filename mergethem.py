

import pandas as pd
import numpy as np
import os
import geopandas as gpd

from shapely.geometry import Point, Polygon
# Open the port cords pickle file
port_cords = pd.read_pickle('./port_coords')
month = 11
year = 2023
# Read the data
data_static = pd.read_csv(f'./grouped_data_static_by_month/{year}/{month}.csv')
# data_static= pd.read_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static_by_month/test_static.csv')
data_static['TimeUtc'] = pd.to_datetime(data_static['TimeUtc'])
def assign_location(point, polygons):
    for location, poly in polygons.items():
        if point.within(poly):
            return location
    return None
chunksize = 10000000
# invert coords
port_cords = {name: [(y, x) for x, y in coords] for name, coords in port_cords.items()}
gdf_polygons = gpd.GeoDataFrame({
    'Location': port_cords.keys(),
    'geometry': [Polygon(coords) for coords in port_cords.values()]
})
gdf_polygons['centroid'] = gdf_polygons.centroid
gdf_centroids = gpd.GeoDataFrame(geometry=gdf_polygons['centroid'])
for dataframe in pd.read_csv(f'./grouped_data_position_by_month/{year}/{month}.csv', chunksize=chunksize):
# for dataframe in pd.read_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month/test_position.csv', chunksize=chunksize):
    data_position = gpd.GeoDataFrame(dataframe, geometry=gpd.points_from_xy(dataframe.Longitude, dataframe.Latitude))
    # data_position = pd.read_csv('./grouped_data_position_by_month/2023.0/11.0.csv')

    for index, row in data_position.iterrows():
        # Calculate the distance to each centroid
        distances = gdf_polygons['centroid'].distance(row['geometry'])
    
        # Find the index of the minimum distance
        closest_index = distances.idxmin()
    
        # Assign the corresponding location to the point
        data_position.at[index, 'Location'] = gdf_polygons.loc[closest_index, 'Location']
    # Merge the data
    data_position = pd.DataFrame(data_position)
    data_position.drop(columns=['geometry'], inplace=True)
    data_position['TimeUtc'] = pd.to_datetime(data_position['TimeUtc'])
    # os.makedirs('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged', exist_ok=True, recursive=True)

    data_position_grouped = data_position.groupby('MMSI')
    data_static_grouped = data_static.groupby('MMSI')
    for name, group in data_position_grouped:
        group = group.sort_values(by='TimeUtc')
        
    for name, group in data_static_grouped:
        group = group.sort_values(by='TimeUtc')
    
    final_df = pd.DataFrame() 
    for name, group in data_position_grouped:
        try:
            # merged = pd.merge(group, data_static_grouped.get_group(name), on='MMSI', how='inner')
            # merged = pd.merge_asof(group, data_static_grouped.get_group(name), on='TimeUtc', by='MMSI', direction='nearest')
            group_min_date = group['TimeUtc'].min()
            group_max_date = group['TimeUtc'].max()
            # from static data get the data that is between the min and max date of the position data
            data_static_grouped.get_group(name)['TimeUtc'] = pd.to_datetime(data_static_grouped.get_group(name)['TimeUtc'])
            static_group = data_static_grouped.get_group(name)[(data_static_grouped.get_group(name)['TimeUtc'] >= group_min_date) & (data_static_grouped.get_group(name)['TimeUtc'] <= group_max_date)]
            merged = pd.concat([group, static_group], axis=0, ignore_index=True,sort=False )
            merged = merged.sort_values(by='TimeUtc')
            merged.to_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/merged.csv', index=False)
            merged.ffill(inplace=True)
            merged.bfill(inplace=True)
            # from megrged drop the rows that have message type ShipStaticData
            merged = merged[merged['MessageType'] != 'ShipStaticData']
            # drop the message type column
            merged.drop(columns=['MessageType'], inplace=True)
            # drop the year and month columns
            merged.drop(columns=['year', 'month'], inplace=True)
            # rename the TimeUtc column to Timestamp and the Timestamp column to ship_timestamp and AssignedLocation to Location
            merged.rename(columns={'TimeUtc': 'Timestamp', 'Timestamp': 'Ship_timestamp'}, inplace=True)
            grouped_by_location=merged.groupby('Location')
            for port , group in grouped_by_location:
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month', exist_ok=True)
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged', exist_ok=True)
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}', exist_ok=True)
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}', exist_ok=True)
                # os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/{port}', exist_ok=True)
                file_path = f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/{port}.csv'
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    # Append without headers
                    merged.to_csv(file_path, mode='a', index=False, header=False)
                else:
                    # Write with headers
                    merged.to_csv(file_path, mode='w', index=False, header=True)

        except Exception as e:
            # save the group to a file if it exists append to the file
            os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month', exist_ok=True)
            os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged', exist_ok=True)
            os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}', exist_ok=True)
            os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}', exist_ok=True)
            if os.path.exists(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/did_not_find_static.csv'):
                group.to_csv(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/did_not_find_static.csv', mode='a', index=False, header=False)
            else:
                group.to_csv(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/did_not_find_static.csv', mode='w', index=False, header=True)
            pass