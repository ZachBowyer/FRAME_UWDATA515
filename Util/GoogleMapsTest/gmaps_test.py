import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBZ4qYFC5GQMzxfYDPMhIHTuorS0lnTNLM')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# Validate an address with address validation
addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
                                                    regionCode='US',
                                                    locality='Mountain View', 
                                                    enableUspsCass=True)

print(addressvalidation_result)

#Write static google map to file
f = open("TestMaps/testGMAPS.png", 'wb')
for chunk in gmaps.static_map(size=(400, 400),
                               center=(52.520103, 13.404871),
                               zoom=15):
    if chunk:
        f.write(chunk)
f.close()

47.44326350000001 -122.3015666

