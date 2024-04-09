from glob import glob

from tqdm import tqdm

import pandas as pd

import os

# Get all the files in the directory
mmsis = pd.read_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/AntwerpMMSIs.csv')

static_files = glob('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static_by_month/*/*.csv')

static_dataFrame = pd.DataFrame()

for static_file in tqdm(static_files):
    static_dataFrame = pd.concat([static_dataFrame, pd.read_csv(static_file)], axis=0, ignore_index=True, sort=False)

# only keep the MMSIs that are in the AntwerpMMSIs.csv
static_dataFrame = static_dataFrame[static_dataFrame['MMSI'].isin(mmsis['0'])]
# save the static data to a file
static_dataFrame.to_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static_by_month/Antwerp_Static.csv', index=False)