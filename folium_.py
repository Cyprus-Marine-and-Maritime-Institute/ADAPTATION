from folium import Map, Rectangle, Polygon
import json
from glob import glob
import os
files = glob("./sefs/*.json")
with open('PortsBoundingBoxes.json') as f:
    bbox = json.load(f)
upper_left = bbox['Limassol'][0]
lower_right = bbox['Limassol'][1]
center = [(upper_left[0] + lower_right[0]) / 2, (upper_left[1] + lower_right[1]) / 2]
m = Map(location=center, zoom_start=6)
for file in files:
    with open(file) as f:
        js = json.load(f)
    # print(js)
    if 'data' in js:
        if 'featureCollection' in js['data']:
            if 'features' in js['data']['featureCollection']:
                for feature in js['data']['featureCollection']['features']:
                    Polygon(
                        locations=[(point[1], point[0]) for point in feature['geometry']['coordinates'][0]],
                        color='red',
                        fill=True,
                        fill_opacity=0.1,
                        # on click show name
                        popup=feature['properties']['name']
                        
                    ).add_to(m)
m.save('map.html')
exit()

for key in bbox:
    upper_left = bbox[key][0]
    lower_right = bbox[key][1]
    bounds = [upper_left, lower_right]
    Rectangle(
        bounds=[bounds[0], bounds[1]],
        color='blue',
        fill=True,
        fill_opacity=0.1
    ).add_to(m)
m.save(key + '.html')

