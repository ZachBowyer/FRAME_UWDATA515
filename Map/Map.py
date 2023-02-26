"""
Easy to use interface to generate folium maps for our web app
"""
import googlemaps 
import folium
import json
from datetime import datetime
import requests
import polyline
from uszipcode import SearchEngine, SimpleZipcode, ComprehensiveZipcode
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

def createmap(origin, destinations, directions=True, originMarker=True, destinationMarkers=True, zipCode=None):
    """
    Description: Singular endpoint for fully created map
    Input: 
        origin: String
        destinations: List of strings
    Output: HTML String
    """
    originCoords = getaddresscoordinates(origin)
    
    #Create map
    new_map = folium.Map(location=originCoords)

    if(originMarker == True):
        folium.Marker(originCoords, popup="Origin:"+origin).add_to(new_map)
    
    colors = ["red", "blue", "green", "orange", "darkred", "lightred",
              "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple", "white", 
              "pink", "lightblue", "lightgreen", "gray", "black", "lightgray"]
    index=0
    for destination in destinations:
        destinationCoords = getaddresscoordinates(destination)
        if(destinationMarkers == True):
            folium.Marker(destinationCoords, popup="Destination:"+destination, 
                          icon=folium.Icon(icon="star", color=colors[index]),
                          ).add_to(new_map)
        #Add directions if specified
        if(directions == True):
            directionCoords = getdirections(origin, destination)
            folium.PolyLine(directionCoords, tooltip="?", color=colors[index]).add_to(new_map)
        index += 1

    #Highlight zip code if provided
    if(zipCode is not None):
        search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
        zipcode = search.by_zipcode(zipCode)
        borderpolygon = zipcode.polygon

        #Get coords in orientation folium requires (Lat, Lon) instead of (Lon, Lat)
        newCoords = []
        for coords in borderpolygon:
            newCoords.append([coords[1], coords[0]])
        
        #Draw polygon
        folium.Polygon(
            locations=newCoords,
            popup="Test",
            color = "Green",
            fill=True,
            fill_color = "Green",
            ).add_to(new_map)
    return new_map

#testmap = createmap("4555 Roosevelt Way NE, Seattle, WAS 98105", "6226 Seaview Ave NW, Seattle, WA, 98107")
#testmap = createmap("4555 Roosevelt Way NE, Seattle, WAS 98105", "41st Division Dr, Joint Base Lewis-McChord, WA 98433")
#testmap = createmap("4555 Roosevelt Way NE, Seattle, WAS 98105", ["99338", "6226 Seaview Ave NW, Seattle, WA, 98107"], zipCode=99338)
testmap = createmap("4555 Roosevelt Way NE, Seattle, WAS 98105", ["7501 35th Ave NE, Seattle, WA 98115", 
                                                                  "6226 Seaview Ave NW, Seattle, WA, 98107",
                                                                  "1000 NE Northgate Way, Seattle, WA 98125",
                                                                  "12801 Aurora Ave N, Seattle, WA 98133",
                                                                  "2901 E Madison St, Seattle, WA 98112"],
                                                                  zipCode=None)
testmap.save("Map.html")
#print(getdistanceoftrip("4555 Roosevelt Way NE, Seattle, WAS 98105", "41st Division Dr, Joint Base Lewis-McChord, WA 98433"))
#print(getdurationoftrip("4555 Roosevelt Way NE, Seattle, WAS 98105", "41st Division Dr, Joint Base Lewis-McChord, WA 98433"))
