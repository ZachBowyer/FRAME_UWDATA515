"""
Tests:
"""

import sys
sys.path.insert(0, '../fgmap')
import fgmap 
import unittest
import folium

class TestGoogleMapsMethods(unittest.TestCase):
    """ Tests each function in fgmap.py that is outside of the fgmap class. 
        In general, each function will be tested with the following:
            Smoke test             (See if it runs)
            Input validation       (Throws error if input is not correct type)
            Output validation      (Throws error if output is not correct type)
            Expected value test    (We know the expected output ahead of time)
            Edge cases             (Could be anything needed)
    """
    #######################################################################
    def test_addressexists_smoke(self):
        exists = fgmap.addressexists("93338")
        exists = fgmap.addressexists("A*S&TD876t23987")
        exists = fgmap.addressexists("a9sd8$$uf0u2-09")
        self.assertTrue(True)
    
    #######################################################################
    def test_getaddresscoordinates_smoke(self):
        """See if it runs"""
        directions = fgmap.getaddresscoordinates("4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)
    
    def test_getaddresscoordinates_verifyinput(self):
        """ Make sure getaddresscoordinates() can only take in a string """
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.getaddresscoordinates()")
            fgmap.getaddresscoordinates(99338)
    
    def test_getaddresscoordinates_verifyoutput(self):
        """ Make sure getaddresscoordinates() returns a list with 2 floats"""
        val = fgmap.getaddresscoordinates("99338")
        self.assertIsInstance(val, list, "getaddresscoordinates() did not return a list.")
        self.assertEqual(2, len(val), "getaddresscoordinates() return list did not return list of size=2")
        self.assertIsInstance(val[0], float, "getaddresscoordinates() 1st element did not return a float")
        self.assertIsInstance(val[1], float, "getaddresscoordinates() 2nd element did not return a float")

    def test_getaddresscoordinates_expectation(self):
        """Supply values and compare to expected output"""
        coords1 = fgmap.getaddresscoordinates("99338")
        coords2 = fgmap.getaddresscoordinates("4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertEqual(coords1, [46.1031257, -119.2960196], "getaddresscoordinates() did not return expected value")
        self.assertEqual(coords2, [47.6626101, -122.317593], "getaddresscoordinates() did not return expected value")

    def test_getaddresscoordinates_edge_invalidaddress(self):
        """ Supply address that doesn't exist """
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.getaddresscoordinates()")
            coords2 = fgmap.getaddresscoordinates("a9sd8$$9ads8u-asd-8suf098asduf098u2-09")

    #######################################################################
    def test_getdirections_smoke(self):
        """See if it runs"""
        directions = fgmap.getdirections("99338", "4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)

    def test_getdirections_verifyinput(self):
        """Make sure getdirections() can only take in two strings"""
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for fgmap.getdirections()")
            fgmap.getdirections(99338, "98521")
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for fgmap.getdirections()")
            fgmap.getdirections("99338", 98521)
    
    def test_getdirections_verifyoutput(self):
        """Return should be list of lists and each interior element should be a float"""
        directions = fgmap.getdirections("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertIsInstance(directions, list, "getdirections() did not return a list (outer)")
        for coords in directions:
            self.assertIsInstance(coords, tuple, "getdirections() did not return a tuple (inner)")
            for coord in coords:
                self.assertIsInstance(coord, float, "getdirections() did not return a float (inner-element)")

    def test_getdirections_expectation(self): #What if directions change...
        """Supply values and compare to expected output"""
        directions = fgmap.getdirections("1410 18th Ave, Seattle, WA 98122", "1300 E Pine St, Seattle, WA 98122")
        expectedDirections = [(47.61326, -122.30887), (47.6129, -122.30887), (47.6129, -122.30951), 
                              (47.6129, -122.31034), (47.61291, -122.31148), (47.61292, -122.31413), 
                              (47.61292, -122.3142), (47.61313, -122.3142), (47.61404, -122.31422), 
                              (47.61528, -122.31424), (47.61528, -122.31533)]
        self.assertEqual(directions, expectedDirections, "getdirections() did not return expected value")
    
    def test_getdirections_edge_invalidaddress(self):
        """ Supply address that doesn't exist """
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.getdirections() arg 1")
            directions = fgmap.getdirections("99338", "a9sd8$$uf0u2-09")
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.getdirections() arg 2")
            directions = fgmap.getdirections("a9sd8$$uf0u2-09", "99338")

    #Check if directions dont exist, IE OVERSEAS

    #######################################################################
    def test_getdistanceoftrip_smoke(self):
        """ See if it runs """
        distance = fgmap.getdistanceoftrip("99338", "4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)

    def test_getdistanceoftrip_verifyinput(self):
        """ Should only be able to take in 2 strings """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for fgmap.getdistanceoftrip()")
            fgmap.getdistanceoftrip(99338, "98521")
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for fgmap.getdistanceoftrip()")
            fgmap.getdistanceoftrip("99338", 98521)

    def test_getdistanceoftrip_verifyoutput(self):
        """ Return should be a string """
        distance = fgmap.getdistanceoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertIsInstance(distance, str, "getdistanceoftrip() did not return string")
    
    def test_getdistanceoftrip_expectation(self):
        """ Supply values and compare to expected output """
        distance = fgmap.getdistanceoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertEqual(distance, "231 mi", "getdistanceoftrip() did not return as expected")

    def test_getdistanceoftrip_edge_invalidaddress(self):
        """ Test invalid address """
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.getdistanceoftrip()")
            distance = fgmap.getdistanceoftrip("99338", "a98asduf098u2-09")
    
    #######################################################################
    def test_getdurationoftrip_smoke(self):
        """ See if it runs """
        duration = fgmap.getdurationoftrip("99338", "4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)
    
    def test_getdurationftrip_verifyinput(self):
        """ Should only be able to take in 2 strings """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for fgmap.getdurationoftrip()")
            fgmap.getdurationoftrip(99338, "98521")
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for fgmap.getdurationoftrip()")
            fgmap.getdurationoftrip("99338", 98521)

    def test_getdurationoftrip_verifyoutput(self):
        """ Return should be a string """
        duration = fgmap.getdurationoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertIsInstance(duration, str, "getdurationoftrip() did not return string")
    
    def test_getdurationoftrip_expectation(self): #What if the route changes...
        """ Should be expected output """ 
        duration = fgmap.getdurationoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertEqual(duration, "3 hours 47 mins", "getdistanceoftrip() did not return as expected")

    def test_getdurationoftrip_edge_invalidaddress(self):
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.getdurationoftrip()")
            duration = fgmap.getdurationoftrip("99338", "a98asduf098u2-09")
    
    ########################################################################
    def test_fgmap_smoke(self):
        """See if it works"""
        newmap = fgmap.Fgmap()
        newmap.createmap(origin="4555 Roosevelt Way NE, Seattle, WAS 98105")
        newmap.addmarker("4555 Roosevelt Way NE, Seattle, WAS 98105")
        newmap.addtrippolyline("99338", "blue")
        newmap.add_simple_multi_destinations(["12813 198th Dr NE, Woodinville, WA 98077", 
                                              "14107 194th Ave NE, Woodinville, WA 98077"])
        newmap.showzipcode(99338)
        mapobjectr = newmap.returnmap()
        outputhtml = newmap.returnhtml()
        self.assertTrue(True)
    
    ########################################################################
    def test_fgmap_createmap_verifyinputs(self):
        newmap = fgmap.Fgmap()
        """ Test inputs for all methods in class"""
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.createmap()")
            newmap.createmap(origin=23198)
    
    def test_fgmap_createmap_verifyoutputs(self):
        """ Test outputs for all methods in class"""
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        self.assertIsInstance(newmap.map, folium.folium.Map, "fgmap.Fgmap.createmap() did not set self.map to folium.folium.map")
    
    def test_fgmap_createmap_edge_invalidaddressorigin(self):
        with self.assertRaises(ValueError):
            newmap = fgmap.Fgmap()
            newmap.createmap(origin = "asd98u9832")
            print("Google cannot find address properly raised for fgmap.Fgmap.createmap()")
    
    #def test_fgmap_createmap_edge_noneorigin(self):
    #    x=1

    #############################################
    def test_fgmap_addmarker_verifyinputs(self):
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.addmarker(); arg: 'address'")
            newmap.addmarker(99338, popup="abc", icon="star", color="blue")
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.addmarker(); arg: 'popup'")
            newmap.addmarker("99338", popup=123, icon="star", color="blue")
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.addmarker(); arg: 'icon'")
            newmap.addmarker("99338", popup="123", icon=123, color="blue")
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.addmarker(); arg: 'color'")
            newmap.addmarker("99338", popup="123", icon="123", color=123.2)
    
    def test_fgmap_addmarker_verifyoutputs(self):
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "93338")
        address = "4555 Roosevelt Way NE, Seattle, WAS 98105"
        newmap.addmarker(address)
        self.assertIsInstance(newmap.markers[address],folium.map.Marker, "fgmap.Fgmap.addmarker() did not set self.markers[] to folium.map.Marker")

    #def test_fgmap_addmarker_edge_invalidaddress(self):
    #    x=1
    
    #def test_fgmap_addmarker_edge_invalidicon(self):
    #    x=1
    
    #def test_fgmap_addmarker_edge_invalidcolor(self):
    #    x=1

    #############################################
    def test_fgmap_addtrippolyline_verifyinputs(self):
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.addtripolyline(); arg: 'address'")
            newmap.addtrippolyline(99338, "blue")
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.addtripolyline(); arg: 'color'")
            newmap.addtrippolyline("99338", 32443)
    
    def test_fgmap_addtrippolyline_verifyoutputs(self):
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        address = "4555 Roosevelt Way NE, Seattle, WAS 98105"
        newmap.addtrippolyline(address, "blue")
        print(newmap.polylines[address])
        self.assertIsInstance(newmap.polylines[address], folium.vector_layers.PolyLine, "fgmap.Fgmap.addtrippolyline() did not set self.polyLines[] to folium.vector_layers.Polyline")

    #Edge case where both origin and a single address are the same!

    #def test_fgmap_addtrippolyline_edge_invalidaddress(self):
    #    x=1
    
    #def test_fgmap_addtrippolyline_edge_invalidcolor(self):
    #    x=1

    #############################################
    def test_fgmap_simplemultidestinations_verifyinputs(self):
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Non list input error properly raised for fgmap.fgmap.simplemultidestinations()")
            newmap.add_simple_multi_destinations("12813 198th Dr NE, Woodinville, WA 98077")
    
    #def test_fgmap_addsimplemultidestinations_edge_invalidaddress(self):
    #    x=1

    #############################################
    def test_showzipcode_verifyinputs(self):
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Non integer input error properly raised for fgmap.fgmap.showzipcode(); arg: 'zipcodenum'")
            newmap.showzipcode("99338")
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.showzipcode(); arg: 'color'")
            newmap.showzipcode(93338, color=193)

    #def test_fgmap_showzipcode_edge_invalidzipcode(self):
    #    x=1

    #def test_fgmap_showzipcode_edge_invalidcolor(self):
    #    x=1

if __name__ == '__main__':
    unittest.main()