from glob import glob
from tqdm import tqdm
import pandas as pd
import os
# Get all the files in the directory
antwerpMMSIs = set()
antwerpFiles = glob('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port/*/*/Antwerp.csv')
print(antwerpFiles)
for antwerpFile in tqdm(antwerpFiles):
    for antwerpData in tqdm(pd.read_csv(antwerpFile, chunksize=1000000)):
        antwerpMMSIs.update(antwerpData['MMSI'].unique())
    
    print(len(antwerpMMSIs))
antwerpMMSIs = pd.DataFrame(antwerpMMSIs)
antwerpMMSIs.to_csv('/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_merged_by_month/merged/AntwerpMMSIs.csv', index=False)

