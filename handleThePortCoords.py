import pandas as pd


pckled_file=pd.read_pickle('./port_coords')
# Inspect the first few items to understand the structure
# Convert each list in the dictionary to a string
for key in pckled_file.keys():
    pckled_file[key] = str(pckled_file[key])
# Now create a DataFrame from the modified dictionary
dtframe = pd.DataFrame(list(pckled_file.items()), columns=['Port', 'Coordinates'])


dtframe.to_csv('port_coords.csv',index=False)