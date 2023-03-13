""" Tests each method in fgmap/fgmap.py 
    run via python test_fgmap.py
    The output messages let you know when specific tests pass
"""
# Ignoring first because we dont want to set everyone's python PATH or pylintr
# Ignoring second because the redundancy is a way to prove functions worked
# Ignoring third because its bad practice to unittest privated methods
#          also prefer to split testing into many functions
# pylint: disable=import-error, redundant-unittest-assert, too-many-public-methods

import sys
import unittest
import folium
sys.path.insert(0, '../fgmap')
# (Need this because we don't want to edit everyones PYTHONPATH)
# pylint: disable=wrong-import-position
import fgmap

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
        """ See if fgmap.addressexists() works """
        fgmap.addressexists("93338")
        fgmap.addressexists("A*S&TD876t23987")
        fgmap.addressexists("a9sd8$$uf0u2-09")
        self.assertTrue(True)

    #######################################################################
    def test_getaddresscoordinates_smoke(self):
        """See if fgmap.addresscoordinates() works"""
        fgmap.getaddresscoordinates("4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)

    def test_getaddresscoordinates_verifyinput(self):
        """ Expected input for fgmap.getaddresscoordinates(): string """
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.getaddresscoordinates()")
            fgmap.getaddresscoordinates(99338)

    def test_getaddresscoordinates_verifyoutput(self):
        """ Expected outputs for fgmap.getaddresscoordinates(): List of 2 floats"""
        val = fgmap.getaddresscoordinates("99338")
        self.assertIsInstance(val, list, "getaddresscoordinates() did not return a list.")
        self.assertEqual(2, len(val),
            "getaddresscoordinates() return list did not return list of size=2")
        self.assertIsInstance(val[0], float,
            "getaddresscoordinates() 1st element did not return a float")
        self.assertIsInstance(val[1], float,
            "getaddresscoordinates() 2nd element did not return a float")

    def test_getaddresscoordinates_expectation(self):
        """ Compare to expected output """
        coords1 = fgmap.getaddresscoordinates("99338")
        coords2 = fgmap.getaddresscoordinates("4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertEqual(coords1, [46.1031257, -119.2960196],
            "getaddresscoordinates() did not return expected value")
        self.assertEqual(coords2, [47.6626101, -122.317593],
        "getaddresscoordinates() did not return expected value")

    def test_getaddresscoordinates_edge_invalidaddress(self):
        """ Supply address that doesn't exist """
        with self.assertRaises(ValueError):
            print("""Google cannot find address error properly
                  raised for fgmap.getaddresscoordinates()""")
            fgmap.getaddresscoordinates("a9sd8$$9ads8u-asd-8suf098asduf098u2-09")

    #######################################################################
    def test_getdirections_smoke(self):
        """See if fgmap.getdirections() works"""
        fgmap.getdirections("99338", "4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)

    def test_getdirections_verifyinput(self):
        """ Expected input for fgmap.getdirections(): String, string """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for fgmap.getdirections()")
            fgmap.getdirections(99338, "98521")
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for fgmap.getdirections()")
            fgmap.getdirections("99338", 98521)

    def test_getdirections_verifyoutput(self):
        """ Expected output for fgmap.getdirections(): List of list of floats """
        directions = fgmap.getdirections("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertIsInstance(directions, list, "getdirections() did not return a list (outer)")
        for coords in directions:
            self.assertIsInstance(coords, tuple, "getdirections() did not return a tuple (inner)")
            for coord in coords:
                self.assertIsInstance(coord, float,
                "getdirections() did not return a float (inner-element)")

    def test_getdirections_expectation(self): #What if directions change...
        """ Compare to expected output """
        directions = fgmap.getdirections("1410 18th Ave, Seattle, WA 98122",
                                        "1300 E Pine St, Seattle, WA 98122")
        expected_directions = [(47.61326, -122.30887), (47.6129, -122.30887), (47.6129, -122.30951),
                              (47.6129, -122.31034), (47.61291, -122.31148), (47.61292, -122.31413),
                              (47.61292, -122.3142), (47.61313, -122.3142), (47.61404, -122.31422),
                              (47.61528, -122.31424), (47.61528, -122.31533)]
        self.assertEqual(directions, expected_directions,
                        "getdirections() did not return expected value")

    def test_getdirections_edge_invalidaddress(self):
        """ Supply address that doesn't exist """
        with self.assertRaises(ValueError):
            print("""Google cannot find address error properly raised
                 for fgmap.getdirections(); arg: 'origin'""")
            fgmap.getdirections("99338", "a9sd8$$uf0u2-09")
        with self.assertRaises(ValueError):
            print("""Google cannot find address error properly raised
                  for fgmap.getdirections(); arg: 'destination'""")
            fgmap.getdirections("a9sd8$$uf0u2-09", "99338")

    #Check if directions dont exist, IE OVERSEAS
    def test_getdirections_edge_addressoverseas(self):
        """ Overseas directions cannot be made """
        with self.assertRaises(ValueError):
            print("""Google cannot create overseas direcitons error properly raised
                  for fgmap.getdirections()""")
            fgmap.getdirections("93338", "99338")

    #######################################################################
    def test_getdistanceoftrip_smoke(self):
        """ See if fgmap.getdistanceoftrip() runs """
        fgmap.getdistanceoftrip("99338", "4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)

    def test_getdistanceoftrip_verifyinput(self):
        """ Expected input for fgmap.getdistanceoftrip(): String, string """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for fgmap.getdistanceoftrip()")
            fgmap.getdistanceoftrip(99338, "98521")
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for fgmap.getdistanceoftrip()")
            fgmap.getdistanceoftrip("99338", 98521)

    def test_getdistanceoftrip_verifyoutput(self):
        """ Expected output of fgmap.getdistanceoftrip(): String"""
        distance = fgmap.getdistanceoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertIsInstance(distance, str, "getdistanceoftrip() did not return string")

    # As of 3/10/2023, a similar function had a very slight change. The same issue applies here.
    # Therefore, this expectation test will never be 100% fool proof, so we will need to remove it
    #def test_getdistanceoftrip_expectation(self):
    #    """ Compare to expected output """ #This will probably slightly change
    #    distance = fgmap.getdistanceoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
    #    self.assertEqual(distance, "231 mi", "getdistanceoftrip() did not return as expected")

    def test_getdistanceoftrip_edge_invalidaddress(self):
        """ Test invalid address """
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.getdistanceoftrip()")
            fgmap.getdistanceoftrip("99338", "a98asduf098u2-09")

    #######################################################################
    def test_getdurationoftrip_smoke(self):
        """ See if fgmap.getdurationoftrip() runs """
        fgmap.getdurationoftrip("99338", "4555 Roosevelt Way NE, Seattle, WAS 98105")
        self.assertTrue(True)

    def test_getdurationftrip_verifyinput(self):
        """ Expected input for fgmap.getdurationoftrip(): String, string """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for fgmap.getdurationoftrip()")
            fgmap.getdurationoftrip(99338, "98521")
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for fgmap.getdurationoftrip()")
            fgmap.getdurationoftrip("99338", 98521)

    def test_getdurationoftrip_verifyoutput(self):
        """ Expected input for fgmap.getdurationoftrip(): String """
        duration = fgmap.getdurationoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
        self.assertIsInstance(duration, str, "getdurationoftrip() did not return string")

    # As of 3/10/2023, the return went from 3 hours 47 minutes to 3 hours 48 minutes,
    #  this is likely due to a small change in traffic
    #  Therefore, this expectation test will never be 100% fool proof, so we will need to remove it
    #def test_getdurationoftrip_expectation(self):
    #    """ Expected output for fgmap.getdurationoftrip(): String """
    #    duration = fgmap.getdurationoftrip("99338", "1300 E Pine St, Seattle, WA 98122")
    #    self.assertEqual(duration, "3 hours 47 mins",
    #                    "getdistanceoftrip() did not return as expected")

    def test_getdurationoftrip_edge_invalidaddress(self):
        """ Test invalid address """
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.getdurationoftrip()")
            fgmap.getdurationoftrip("99338", "a98asduf098u2-09")

    ########################################################################
    def test_fgmap_smoke(self):
        """ See if most fgmap.fgmap() functions run """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin="4555 Roosevelt Way NE, Seattle, WAS 98105")
        newmap.addmarker("4555 Roosevelt Way NE, Seattle, WAS 98105")
        newmap.addtrippolyline("99338", "blue")
        newmap.add_simple_multi_destinations(["12813 198th Dr NE, Woodinville, WA 98077",
                                              "14107 194th Ave NE, Woodinville, WA 98077"])
        newmap.showzipcode(99338)
        newmap.returnmap()
        newmap.returnhtml()
        self.assertTrue(True)

    ########################################################################
    def test_fgmap_createmap_verifyinputs(self):
        """ Expected input for fgmap.Fgmap.createmap(): String"""
        newmap = fgmap.Fgmap()
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.createmap(), origin")
            newmap.createmap(origin=23198)
        with self.assertRaises(ValueError):
            print("Non string input error properly raised for fgmap.fgmap.createmap(), zoom")
            newmap.createmap(origin="99338", zoom_start="10")

    def test_fgmap_createmap_verifyoutputs(self):
        """ Expected output for fgmap.Fgmap.createmap(): folium.folium.map """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        self.assertIsInstance(newmap.map, folium.folium.Map,
                             "fgmap.Fgmap.createmap() did not set self.map to folium.folium.map")

    def test_fgmap_createmap_edge_invalidaddressorigin(self):
        """ Test invalid address """
        with self.assertRaises(ValueError):
            print("Google cannot find address properly raised for fgmap.Fgmap.createmap()")
            newmap = fgmap.Fgmap()
            newmap.createmap(origin = "asd98u9832")

    #############################################
    def test_fgmap_addmarker_verifyinputs(self):
        """ Expected inputs for fgmap.Fgmap.addmarker(): String, string, string, string"""
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("""Non string input error properly raised for
                   fgmap.fgmap.addmarker(); arg: 'address'""")
            newmap.addmarker(99338, popup="abc", icon="star", color="blue")
        with self.assertRaises(ValueError):
            print("""Non string input error properly raised for
                   fgmap.fgmap.addmarker(); arg: 'popup'""")
            newmap.addmarker("99338", popup=123, icon="star", color="blue")
        with self.assertRaises(ValueError):
            print("""Non string input error properly raised for
                  fgmap.fgmap.addmarker(); arg: 'icon'""")
            newmap.addmarker("99338", popup="123", icon=123, color="blue")
        with self.assertRaises(ValueError):
            print("""Non string input error properly raised for
                   fgmap.fgmap.addmarker(); arg: 'color'""")
            newmap.addmarker("99338", popup="123", icon="123", color=123.2)

    def test_fgmap_addmarker_verifyoutputs(self):
        """ Expected output for fgmap.Fgmap.addmarker(): folium.map.marker """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "93338")
        address = "4555 Roosevelt Way NE, Seattle, WAS 98105"
        newmap.addmarker(address)
        self.assertIsInstance(newmap.markers[address],folium.map.Marker,
            "fgmap.Fgmap.addmarker() did not set self.markers[] to folium.map.Marker")

    def test_fgmap_addmarker_edge_invalidaddress(self):
        """ Test invalid address """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Google cannot find address error properly raised for fgmap.Fgmap.addmarker()")
            newmap.addmarker("98sz7dtf8796we")

    def test_fgmap_addmarker_edge_invalidcolor(self):
        """ Test invalid color """
        with self.assertRaises(ValueError):
            print("""Color does not exist error properly raised for
                  fgmap.Fgmap.addmarker(); arg: 'color'""")
            newmap = fgmap.Fgmap()
            newmap.createmap(origin = "99338")
            newmap.addmarker("99338", icon="star", color="asdds")

    #############################################
    def test_fgmap_addtrippolyline_verifyinputs(self):
        """ Expected inputs for fgmap.Fgmap.addtrippolyline(): String, String """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("""Non string input error properly raised for
                  fgmap.fgmap.addtripolyline(); arg: 'address'""")
            newmap.addtrippolyline(99338, "blue")
        with self.assertRaises(ValueError):
            print("""Non string input error properly raised for
                  fgmap.fgmap.addtripolyline(); arg: 'color'""")
            newmap.addtrippolyline("99338", 32443)

    def test_fgmap_addtrippolyline_verifyoutputs(self):
        """ Expected output for fgmap.Fgmap.addtrippolyline(): self.map should be changed """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        address = "4555 Roosevelt Way NE, Seattle, WAS 98105"
        newmap.addtrippolyline(address, "blue")
        self.assertIsInstance(newmap.polylines[address], folium.vector_layers.PolyLine,
        "fgmap.Fgmap.addtrippolyline() did not set self.polyLines to folium.vector_layers.Polyline")

    def test_fgmap_addtrippolyline_edge_sameaddresses(self):
        """ Test if both addresses are the same """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        address = "99338"
        with self.assertRaises(ValueError):
            print("Address same as origin error properly raised for fgmap.Fgmap.addtrippolyline()")
            newmap.addtrippolyline(address, "blue")

    def test_fgmap_addtrippolyline_edge_invalidaddress(self):
        """ Test invalid address """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        address = "90as8y222---d987"
        with self.assertRaises(ValueError):
            print("Invalid address error properly raised for fgmap.Fgmap.addtrippolyline()")
            newmap.addtrippolyline(address, "blue")

    def test_fgmap_addtrippolyline_edge_invalidcolor(self):
        """ Test invalid color """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        address = "4555 Roosevelt Way NE, Seattle, WAS 98105"
        with self.assertRaises(ValueError):
            print("Color does not exist error properly raised for fgmap.Fgmap.addtrippolyline()")
            newmap.addtrippolyline(address, "09ads8y087y")

    #############################################
    def test_fgmap_simplemultidestinations_verifyinputs(self):
        """ Expected inputs for fgmap.Fgmap.simplemultidestinations(): List of strings """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Non list input error properly raised for fgmap.fgmap.simplemultidestinations()")
            newmap.add_simple_multi_destinations("12813 198th Dr NE, Woodinville, WA 98077")

    def test_fgmap_addsimplemultidestinations_edge_invalidaddress(self):
        """ Test invalid address """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("""Google maps could not find address error
                  properly raised for fgmap.Fgmap.addsimplemultidestinations()""")
            newmap.add_simple_multi_destinations(["12813 198th Dr NE, Woodinville, WA 98077",
                                                  "w---asd9i"])

    #############################################
    def test_showzipcode_verifyinputs(self):
        """ Expected inputs for fgmap.Fgmap.showzipcode(): Integer, string """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("""Non integer input error properly raised for
                  fgmap.fgmap.showzipcode(); arg: 'zipcodenum'""")
            newmap.showzipcode("99338")
        with self.assertRaises(ValueError):
            print("""Non string input error properly raised for
                  fgmap.fgmap.showzipcode(); arg: 'color'""")
            newmap.showzipcode(93338, color=193)

    def test_fgmap_showzipcode_edge_invalidzipcode(self):
        """ Test invalid address """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Invalid zip code error properly raised for fgmap.Fgmap.showzipcode()")
            newmap.showzipcode(91287349218732199338)

    def test_fgmap_showzipcode_edge_invalidcolor(self):
        """ Test invalid color """
        newmap = fgmap.Fgmap()
        newmap.createmap(origin = "99338")
        with self.assertRaises(ValueError):
            print("Invalid color error properly raised for fgmap.Fgmap.showzipcode()")
            newmap.showzipcode(99338, color="opaisdjh")

if __name__ == '__main__':
    unittest.main()
