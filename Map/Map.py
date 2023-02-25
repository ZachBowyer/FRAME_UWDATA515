"""
Easy to use interface to generate folium maps for our web app
"""
import googlemaps 
import folium
import json
from datetime import datetime
import requests
import polyline
gmaps = googlemaps.Client(key='AIzaSyBZ4qYFC5GQMzxfYDPMhIHTuorS0lnTNLM')

# https://googlemaps.github.io/google-maps-services-python/docs/index.html#googlemaps.Client.addressvalidation

#def addressexist():
#    """
#    Input: String (Google maps valid address)
#    Output: Boolean (True if google maps can find the specified input, false otherwise)
#    """
#    test = gmaps.addressvalidation(["4555 Roosevelt Way NE, Seattle, WAS 98105"], 
#                                regionCode='US',
#                                locality='None', 
#                                enableUspsCass=True)
#    print(json.dumps(test, sort_keys=True, indent=4))
#    #print(test)
#    return True

def getaddresscoordinates(address):
    """
    Description: 
        Given a valid google maps address, return its coordinates (latitude and longitude)
    Input:
        address-String that is a google maps valid address
    Output:
        List of two signed floats: [latitude, longitude] 
    """
    info = gmaps.addressvalidation(address)
    lat = info["result"]["geocode"]["location"]["latitude"]
    lon = info["result"]["geocode"]["location"]["longitude"]
    return [lat, lon]

def getdirections(origin, destination):
    """
    Description: 
        Returns a list of lists containing the coordinates for a trip 
    Input: 
        origin-String that is a googlemaps valid address
        destination-String that is a googlemaps valid address
    Output: 
        List of lists: IE: [[123, 20], [129, 21], ...]
    """
    now = datetime.now()
    directions = gmaps.directions(origin, destination, mode="driving", departure_time=now)
    polylineEncode = directions[0]["overview_polyline"]["points"]
    coordinates = polyline.decode(polylineEncode, 5)
    #print(json.dumps(directions, sort_keys=True, indent=2))
    return coordinates

def getdistanceoftrip(origin, destination):
    """
    Description:
        Given two valid google maps addresses, returns estimated trip distance
    Inputs:
        origin-String that is a googlemaps valid address
        destination-String that is a googlemaps valid address
    Outputs: 
        String
    """
    directions = gmaps.directions(origin, destination, mode="driving")
    return directions[0]["legs"][0]["distance"]["text"]

def getdurationoftrip(origin, destination):
    """
    Description:
        Given two valid google maps addresses, returns estimated trip duration
    Inputs:
        origin-String that is a googlemaps valid address
        destination-String that is a googlemaps valid address
    Outputs: 
        String
    """
    directions = gmaps.directions(origin, destination, mode="driving")
    return directions[0]["legs"][0]["duration"]["text"]

def createmap(origin, destination, directions=True, originMarker=True, destinationMarker=True):
    """
    Description: Singular endpoint for fully created map
    Input: ?
    Output: HTML String
    """
    originCoords = getaddresscoordinates(origin)
    destinationCoords = getaddresscoordinates(destination)
    
    #Create map
    new_map = folium.Map(location=originCoords)

    if(originMarker == True):
        folium.Marker(originCoords, popup="Origin:"+origin).add_to(new_map)
    
    if(destinationMarker == True):
        folium.Marker(destinationCoords, popup="Destination:"+destination).add_to(new_map)

    #Add directions if specified
    if(directions == True):
        directionCoords = getdirections(origin, destination)
        folium.PolyLine(directionCoords, tooltip="?").add_to(new_map)
    return new_map

#testmap = createmap("4555 Roosevelt Way NE, Seattle, WAS 98105", "6226 Seaview Ave NW, Seattle, WA, 98107")
#testmap = createmap("4555 Roosevelt Way NE, Seattle, WAS 98105", "41st Division Dr, Joint Base Lewis-McChord, WA 98433")
testmap = createmap("4555 Roosevelt Way NE, Seattle, WAS 98105", "99338")
testmap.save("Map.html")
#print(getdistanceoftrip("4555 Roosevelt Way NE, Seattle, WAS 98105", "41st Division Dr, Joint Base Lewis-McChord, WA 98433"))
#print(getdurationoftrip("4555 Roosevelt Way NE, Seattle, WAS 98105", "41st Division Dr, Joint Base Lewis-McChord, WA 98433"))