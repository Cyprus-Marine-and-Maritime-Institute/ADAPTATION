from glob import glob
import pandas as pd
import os
from tqdm import tqdm
# Get all the files in the directory
dynamicFiles = glob('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port/*/*/*.csv')
staticdata={}
staticFiles = glob('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static_by_month/*/*.csv')

static_dataFrame = pd.DataFrame()
print('Loading static data')
# for staticFile in tqdm(staticFiles):
#     static_dataFrame = pd.concat([static_dataFrame, pd.read_csv(staticFile)], axis=0, ignore_index=True, sort=False)
static_dataFrame=pd.read_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static_by_month/Antwerp_Static.csv')
static_dataFrame['TimeUtc'] = pd.to_datetime(static_dataFrame['TimeUtc'])
data_static_grouped = static_dataFrame.groupby('MMSI')

print('Loaded static data')
for dynamicFile in tqdm(dynamicFiles):
    year=dynamicFile.split('/')[-3]
    month=dynamicFile.split('/')[-2]
    port = dynamicFile.split('/')[-1].split('.')[0]
    if port != 'Antwerp':
        continue
    if year == '2023':
        continue
    print(f'Processing {dynamicFile}')
    for data in pd.read_csv(dynamicFile, chunksize=10000000):
        print(f"Loaded {dynamicFile}")
        # if year+month+port not in staticdata:
        #     staticdata={}
        #     staticdata[year+month+port]= pd.read_csv(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static_by_month/{year}/{month}.csv')
        print(f"Loaded Static {year+month+port}")
        data['TimeUtc'] = pd.to_datetime(data['TimeUtc'])
        grouped_by_mmsi = data.groupby('MMSI')
        # staticdata[year+month+port]['TimeUtc'] = pd.to_datetime(staticdata[year+month+port]['TimeUtc'])
        for name, group in grouped_by_mmsi:
        # try:
            # merged = pd.merge(group, data_static_grouped.get_group(name), on='MMSI', how='inner')
            # merged = pd.merge_asof(group, data_static_grouped.get_group(name), on='TimeUtc', by='MMSI', direction='nearest')
            group_min_date = group['TimeUtc'].min()
            group_max_date = group['TimeUtc'].max()
            # from static data get the data that is between the min and max date of the position data
            if name in data_static_grouped.groups:
                static_group = data_static_grouped.get_group(name)[(data_static_grouped.get_group(name)['TimeUtc'] >= group_min_date) & (data_static_grouped.get_group(name)['TimeUtc'] <= group_max_date)]
            else:
                # save the group to a file if it exists append to the file
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month', exist_ok=True)
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged', exist_ok=True)
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}', exist_ok=True)
                os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}', exist_ok=True)
                if os.path.exists(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/did_not_find_static_{port}.csv'):
                    group.to_csv(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/did_not_find_static_{port}.csv', mode='a', index=False, header=False)
                else:
                    group.to_csv(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/{year}/{month}/did_not_find_static_{port}.csv', mode='w', index=False, header=True)
                pass
            merged = pd.concat([group, static_group], axis=0, ignore_index=True,sort=False )
            merged = merged.sort_values(by='TimeUtc')
            # merged.to_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/merged.csv', index=False)
            merged.ffill(inplace=True)
            merged.bfill(inplace=True)
            # from megrged drop the rows that have message type ShipStaticData
            merged = merged[merged['MessageType'] != 'ShipStaticData']
            # drop the message type column
            merged.drop(columns=['MessageType'], inplace=True)
            # drop the year and month columns
            if 'year' in merged.columns:
                merged.drop(columns=['year'], inplace=True)
            if 'month' in merged.columns:
                merged.drop(columns=['month'], inplace=True)
            # rename the TimeUtc column to Timestamp and the Timestamp column to ship_timestamp and AssignedLocation to Location
            merged.rename(columns={'TimeUtc': 'Timestamp', 'Timestamp': 'Ship_timestamp'}, inplace=True)
            grouped_by_location=merged.groupby('Tags')
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
