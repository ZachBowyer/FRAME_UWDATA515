"""
Script tests out the python library 'Folium'
https://python-visualization.github.io/folium/
The end goal here to compare this tool to the google maps api
Results will be recorded as the technology presentation
"""
import folium
import json
import requests

# Create basic folium map object centered at given coordinates
m = folium.Map(location=[45.5236, -122.6750])

# Save it to html
m.save("TestMaps/basicMap.html")

# Create basic folium map obect centered at given coordinates and zoomed in
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
m.save("TestMaps/basicMapZoomed.html")

# Add marker to folium map with tooltip/popup
folium.Marker([45.5236, -122.6750], popup="<b> Test </b>", tooltip="CLICK").add_to(m)
m.save("TestMaps/basicMapWithMarker.html")

# Marker styles
# Icons - ~22k icons at https://fontawesome.com/icons, refer by the string name on site
m = folium.Map(location=[45.5236, -122.6750])
folium.Marker(
    location=[45.5236, -122.6750],
    popup="test",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

#Different icon (and color)
folium.Marker(
    location=[45.4636, -122.6750],
    popup="test",
    icon=folium.Icon(icon="heart", color="pink"),
).add_to(m)

# Color
folium.Marker(
    location=[45.4236, -122.6750],
    popup="test",
    icon=folium.Icon(color="green"),
).add_to(m)

# Angle
folium.Marker(
    location=[45.4636, -122.8750],
    popup="test",
    icon=folium.Icon(icon="heart", color="green", angle=180),
).add_to(m)

m.save("TestMaps/basicMapWithMultipleMarkers.html")

# Circles and Circle markers
m = folium.Map(location=[45.5236, -122.6750])
folium.Circle(
    radius=100,
    location=[45.5244, -122.6699],
    popup="Test",
    color="crimson",
    fill=False,
).add_to(m)
folium.CircleMarker(
    location=[45.5215, -122.6261],
    radius=50,
    popup="Park",
    color="#3186cc",
    fill=True,
    fill_color="#3186cc",
).add_to(m)
m.save("TestMaps/basicMapWithCircles.html")

# Add lat/lon popup (Click on the map)
m = folium.Map(location=[46.1991, -122.1889], tiles="Stamen Terrain", zoom_start=13)
m.add_child(folium.LatLngPopup())
m.save("TestMaps/latlonPopup.html")

# Users adding markers
m = folium.Map(location=[46.8527, -121.7649], tiles="Stamen Terrain", zoom_start=13)
folium.Marker([46.8354, -121.7325], popup="Camp Muir").add_to(m)
m.add_child(folium.ClickForMarker(popup="Waypoint"))
m.save("TestMaps/UserMarkers.html")

# Polylines
m = folium.Map(location=[-71.38, -73.9], zoom_start=11)
trail_coordinates = [
    (-71.351871840295871, -73.655963711222626),
    (-71.374144382613707, -73.719861619751498),
    (-71.391042575973145, -73.784922248007007),
    (-71.400964450973134, -73.851042243124397),
    (-71.402411391077322, -74.050048183880477),
]
folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)
m.save("TestMaps/PolyLines.html")

#Graph popups
url = ("https://raw.githubusercontent.com/python-visualization/folium/main/examples/data")
vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
vis2 = json.loads(requests.get(f"{url}/vis2.json").text)
vis3 = json.loads(requests.get(f"{url}/vis3.json").text)

m = folium.Map(location=[46.3014, -123.7390], zoom_start=7, tiles="Stamen Terrain")
folium.Marker(
    location=[47.3489, -124.708],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis1, width=450, height=250)
    ),
).add_to(m)
folium.Marker(
    location=[44.639, -124.5339],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis2, width=450, height=250)
    ),
).add_to(m)
folium.Marker(
    location=[46.216, -124.1280],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis3, width=450, height=250)
    ),
).add_to(m)
m.save("TestMaps/graphPopups.html")