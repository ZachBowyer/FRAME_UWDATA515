"""
Easy to use interface to generate folium maps for our web app
"""
# pylint: disable=import-error
from datetime import datetime
import googlemaps
import folium
import polyline
from uszipcode import SearchEngine
gmaps = googlemaps.Client(key='AIzaSyBZ4qYFC5GQMzxfYDPMhIHTuorS0lnTNLM')

def addressexists(address):
    """
    Description:
        Checks if a supplied address is valid
    Input:
        address-String
    Output:
        Boolean (True if address is recognized by google maps)
    """
    if isinstance(address, str) is False:
        raise ValueError("Input: address - must be a string")
    info = gmaps.addressvalidation(address)
    confirmation = info["result"]["address"]["addressComponents"][0]["confirmationLevel"]
    if confirmation == "CONFIRMED":
        return True
    return False

def getaddresscoordinates(address):
    """
    Description: 
        Given a valid google maps address, return its coordinates (latitude and longitude)
    Input:
        address-String that is a google maps valid address
    Output:
        List of two signed floats: [latitude, longitude] 
    """
    if isinstance(address, str) is False:
        raise ValueError("Input: address - must be a string")
    info = gmaps.addressvalidation(address)
    if not addressexists(address):
        raise ValueError("Google can not find the specified address")
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
        List of tuples: IE: [(123.1, 20.2), (129.3, 21.1), ...]
        Interior elements should be floats
    """
    if isinstance(origin, str) is False:
        raise ValueError("Input: origin - must be a string")
    if isinstance(destination, str) is False:
        raise ValueError("Input: destination - must be a string")
    if not addressexists(origin):
        raise ValueError("Google can not find the specified address (origin)")
    if not addressexists(destination):
        raise ValueError("Google can not find the specified address (destination)")
    now = datetime.now()
    directions = gmaps.directions(origin, destination, mode="driving", departure_time=now)
    if len(directions) == 0:
        raise ValueError("Google cannot find directions, it is likely the addresses are overseas")
    encodedpolyline = directions[0]["overview_polyline"]["points"]
    coordinates = polyline.decode(encodedpolyline, 5)
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
    if isinstance(origin, str) is False:
        raise ValueError("Input: origin - must be a string")
    if isinstance(destination, str) is False:
        raise ValueError("Input: destination - must be a string")
    if not addressexists(origin):
        raise ValueError("Google can not find the specified address (origin)")
    if not addressexists(destination):
        raise ValueError("Google can not find the specified address (destination)")
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
    if isinstance(origin, str) is False:
        raise ValueError("Input: origin - must be a string")
    if isinstance(destination, str) is False:
        raise ValueError("Input: destination - must be a string")
    if not addressexists(origin):
        raise ValueError("Google can not find the specified address (origin)")
    if not addressexists(destination):
        raise ValueError("Google can not find the specified address (destination)")
    directions = gmaps.directions(origin, destination, mode="driving")
    return directions[0]["legs"][0]["duration"]["text"]

class Fgmap():
    """
    Class used to modularly break up the steps of adding icons/polylines/polygons to the map
    Currently there is no known 'good' way to remove icons, polylines, polygons etc.
        Bad solution #1: Re-render the map
        Bad solution #2: Add layercontrol and groupings, set specific group to hidden
        Solution #3: Edit the html of self.map manually
    See https://python-visualization.github.io/folium/ for folium documentation
    """
    def __init__(self):
        """
        Description:
            Define class variables
        """
        self.colors = ["red", "blue", "green", "orange", "darkred", "lightred",
                  "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple", "white", 
                  "pink", "lightblue", "lightgreen", "gray", "black", "lightgray"]
        self.origincoords = [0, 0]
        self.markers = {}
        self.polylines = {}
        self.zipcodepolygons = {}
        self.origin = ""
        self.map = None

    #Class methods:
    def createmap(self, origin="", zoom_start=10):
        """
        Description:
            Creates a folium map centered at the origin
        Inputs:
            origin-String of where the map should be centered, must be googlemaps valid
        Outputs:
            None, creates self.map
        """
        if isinstance(origin, str) is False:
            raise ValueError("Input: origin - must be a string")
        if isinstance(zoom_start, int) is False:
            raise ValueError("Input: zoom_start - must be an integer")
        if not addressexists(origin):
            raise ValueError("Google can not find the specified address (origin)")
        self.origin = origin
        self.origincoords = getaddresscoordinates(origin)
        if origin == "":
            self.map = folium.Map()
        else:
            self.map = folium.Map(location=self.origincoords, zoom_start=zoom_start)

    def addmarker(self, address, popup="", icon="star", color="blue"):
        """
        Description: 
            Adds a marker to the folium map
            See https://fontawesome.com/search?s=solid&f=sharp&o=r for icon information
        Inputs:
            address-String that is a googlemaps valid address
            popup-String that is shown when the user clicks on the marker
            icon-String of what icon you want shown 
            color-String of what color you want the marker to be
        Outputs:
            None, adds marker to self.map
        """
        if isinstance(address, str) is False:
            raise ValueError("Input: address - must be a string")
        if isinstance(popup, str) is False:
            raise ValueError("Input: popup - must be a string")
        if isinstance(icon, str) is False:
            raise ValueError("Input: icon - must be a string")
        if isinstance(color, str) is False:
            raise ValueError("Input: color - must be a string")
        if not addressexists(address):
            raise ValueError("Google can not find the specified address for argument: 'address')")
        if color not in self.colors:
            raise ValueError("Color does not exist:", color)
        addresscoords = getaddresscoordinates(address)
        marker = folium.Marker(addresscoords, popup=popup,icon=folium.Icon(icon=icon, color=color))
        marker.add_to(self.map)
        self.markers[address] = marker

    def addtrippolyline(self, address, color):
        """
        Description:
            Adds a polyline to the folium map from self.origin to supplied destination 
        Inputs:
            address-String that is a googlemaps valid address
            color-String of what color you want the polylines to be
        Outputs:
            None, adds polyline to self.map
        """
        if isinstance(address, str) is False:
            raise ValueError("Input: address - must be a string")
        if isinstance(color, str) is False:
            raise ValueError("Input: color - must be a string")
        if not addressexists(address):
            raise ValueError("Google can not find the specified address (origin):", address)
        if address == self.origin:
            raise ValueError("Cannot find directions to same address!", address, self.origin)
        if color not in self.colors:
            raise ValueError("Color does not exist:", color)
        directioncoords = getdirections(self.origin, address)
        poly = folium.PolyLine(directioncoords, tooltip="?", color=color)
        poly.add_to(self.map)
        self.polylines[address] = poly

    def add_simple_multi_destinations(self, addresses):
        """
        Description:
            Creates markers and polylines related to specified destinations
            Non-customizable, used as a quick and dirty method. If you want
            more customization, see addtrippolyline(), addmarker().
        Inputs:
            addresses-List of strings which are googlemaps valid addresses
        Outputs:
            None, adds markers and polylines to self.map
        """
        if isinstance(addresses, list) is False:
            raise ValueError("Input: addresses - must be a list")
        for address in addresses:
            if not addressexists(address):
                raise ValueError("Google can not find the specified address:", address)
        index = 0
        self.addmarker(self.origin, popup="origin", color="blue")
        for address in addresses:
            if not addressexists(address):
                raise ValueError("Google can not find the specified address:", address)
            self.addtrippolyline(address, color=self.colors[index])
            self.addmarker(address, popup=address, color=self.colors[index])
            index += 1

    def showzipcode(self, zipcodenum, color="blue"):
        """
        Description:
            Creates polygon outline around a zip code and fills it
            When running for the first time, downloads data which is slow 
            (Look into fixing or add to setup)
        Inputs:
            zipcodenum-Integer of the zipcode you want shown on the map
            color-String color of what polygon color you want
        Outputs:
            None, draws polygon on self.map
        """
        if isinstance(zipcodenum, int) is False:
            raise ValueError("Input: zipcodecum - must be a integer")
        if isinstance(color, str) is False:
            raise ValueError("Input: color - must be a string")
        if color not in self.colors:
            raise ValueError("Invalid color")
        search = SearchEngine(simple_or_comprehensive=
                              SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
        zipcode = search.by_zipcode(zipcodenum)
        if zipcode is None:
            raise ValueError("Zipcode cannot be found", zipcodenum)
        borderpolygon = zipcode.polygon

        #Get coords in orientation folium requires (Lat, Lon) instead of (Lon, Lat)
        correctedpolygon = []
        for coords in borderpolygon:
            correctedpolygon.append([coords[1], coords[0]])

        #Draw polygon
        polygon = folium.Polygon(
            locations=correctedpolygon,
            popup=zipcodenum,
            color = color,
            fill=True,
            fill_color = color,
        )
        polygon.add_to(self.map)
        self.zipcodepolygons[zipcodenum] = polygon

    def returnmap(self):
        """
        Description:
            Returns the folium map object stored in this class instance
        """
        return self.map

    def save(self, path):
        """
        Description:
           Saves folium map object to html file 
        """
        self.map.save(path)

    def returnhtml(self):
        """
        Description
            Returns html of rendered folium map
        """
        return self.map.get_root().render()
