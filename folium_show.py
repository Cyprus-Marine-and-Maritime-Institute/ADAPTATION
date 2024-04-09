from glob import glob
import pandas as pd
import pydeck as pdk
import folium
from tqdm import tqdm
import simplekml
ports_polygons = pd.read_csv('port_coords.csv')
chunksize = 100000
m = folium.Map(location=[35.1264, 33.4299], zoom_start=6)
for i,chunk in enumerate(pd.read_csv('./grouped_data_position_by_month_subset/data_visualize.csv', chunksize=chunksize)):

    polygons = []
    for index, row in ports_polygons.iterrows():
        polygons.append({'Port': row['Port'], 'coords': eval(row['Coordinates'])})
        # print(ports_polygons.at[index, 'coords'])
    kml = simplekml.Kml()
    # print("Total points ", len(points))

    points_tuple = []
    for index,row in chunk.iterrows():
        kml.newpoint(name=row['Tags'], coords=[(row['Longitude'], row['Latitude'])])
        if row['Tags'] == '':
            color = 'red'
        else:
            color = 'blue'
        folium.Circle(
            location=[row['Latitude'], row['Longitude']],
            radius=10,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)
    print("Done with points")
    for coords in polygons:
        pol = kml.newpolygon(name=coords['Port'], outerboundaryis=coords['coords'])
        pol.style.linestyle.color = simplekml.Color.red  # Line color
        pol.style.linestyle.width = 5  # Line width
        pol.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.green)  # Fill color with some transparency
        folium.Polygon(
            locations=coords['coords'],
            color='red',
            fill=True,
            fill_opacity=0.1,
            popup=coords['Port']
        ).add_to(m)
        
    print("Done with polygons")
    kml.save(f"Ports_{i}.kml")
    print("Done with kml")
    m.save(f"Ports_{i}.html")