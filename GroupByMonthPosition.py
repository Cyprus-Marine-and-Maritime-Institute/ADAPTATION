

from glob import glob
import os
import pandas as pd
import shutil
from io import StringIO

globbed_files_position = glob('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position/*.csv')  # creates a list of all csv files

for file in globbed_files_position:
    try:
        time_now = pd.Timestamp.now()
        print('Reading file: ',file)
        df = pd.read_csv(file, lineterminator='\x0A')
        # df = pd.read_csv(, lineterminator='\x0A')
        time_after = pd.Timestamp.now()
        print(df.head())
        print('Time to read ',time_after - time_now)
        df['TimeUtc'] = pd.to_datetime(df['TimeUtc'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df['year'] = df['TimeUtc'].dt.year
        df['month'] = df['TimeUtc'].dt.month
        df_grouped_year = df.groupby(df['year'])
        print(df_grouped_year.head())

        os.makedirs('./grouped_data_position_by_month', exist_ok=True)
        for name, group in df_grouped_year:
            os.makedirs(f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month/{str(name)}', exist_ok=True)
            time_now = pd.Timestamp.now()
            grouped_by_month = group.groupby(group['month'])
            print('Grouping by month')
            print(grouped_by_month.head())
            time_after = pd.Timestamp.now()
            print('Time to group by month ',time_after - time_now)
            for month, month_group in grouped_by_month:
                file_path = f'/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month/{str(name)}/{str(month)}.csv'
                time_now = pd.Timestamp.now()
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    # Append without headers
                    month_group.to_csv(file_path, mode='a', index=False, header=False)
                    pass
                else:
                    # Write with headers
                    month_group.to_csv(file_path, mode='w', index=False, header=True)
                    pass
                time_after = pd.Timestamp.now()
                print('Time to write ',time_after - time_now)
        
        os.makedirs('./grouped_data_position/done', exist_ok=True)
        shutil.move(file, './grouped_data_position/done')
    except Exception as e:
        print('Error: ',e)
        continue