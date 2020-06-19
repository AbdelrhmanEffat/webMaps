import folium
import pandas

data = pandas.read_csv("friends.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
state = list(data["STATE"])


def color_producer(i):
    if i == 'QB':
        return 'red'
    elif i == 'QM':
        return 'green'
    else:
        return 'cadetblue'


# creating a map object
map = folium.Map(location=[31.046192, 30.844725], zoom_start=15)
# folium.TileLayer('cartodbpositron').add_to(map)
# https://deparkes.co.uk/2016/06/10/folium-map-tiles/

# adding marker on the map
# best practice is to creat a featuregroup
fgf = folium.FeatureGroup(name='friends')

# use zip fun when iterating in 2 lists at the same time
for lt, ln, nm, st in zip(lat, lon, name, state):
    fgf.add_child(folium.Marker(location=[lt, ln], popup=nm + ' ' + st,
                                icon=folium.Icon(color=color_producer(st))))

'''
This is how we change mareker to circle

for lt, ln, nm, st in zip(lat, lon, name, state):
    fg.add_child(folium.CircleMarker(location=(lt, ln), radius=6,
                                     popup=nm + ' ' + st,
                                     fill_color=color_producer(st),
                                     color='grey', fill=True,
                                     fill_opacity=0.9))
'''

# adding a polygon layer wich stands for population

fgp = folium.FeatureGroup(name='Population')
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                                       else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                       else 'red'}))

map.add_child(fgf)
map.add_child(fgp)

# adding a control layer ... we add it after adding the fg
map.add_child(folium.LayerControl())


map.save('Map1.html')
