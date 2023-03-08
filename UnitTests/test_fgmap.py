import sys
sys.path.insert(0, '../fgmap')
import fgmap 
import unittest


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

#class TestMapMethods(unittest.testcase):
#    def test():
#        x=1
#
#if __name__ == '__main__':
#    unittest.main()

#print(fgmap.getaddresscoordinates("99338"))
#Tests
#newmap = fgmap.Fgmap()
#newmap.createmap(origin="4555 Roosevelt Way NE, Seattle, WAS 98105")
#test = newmap.returnhtml()
#print(test)
#newmap.addmarker("4555 Roosevelt Way NE, Seattle, WAS 98105",
#                popup="Origin", icon="star", color="green")
#newmap.addmarker("1000 NE Northgate Way, Seattle, WA 98125",
#                popup="Destination", icon="star", color="green")
##newmap.addtrippolyline("1000 NE Northgate Way, Seattle, WA 98125", color="green")
#newmap.add_simple_multi_destinations(["7501 35th Ave NE, Seattle, WA 98115",
#                    "6226 Seaview Ave NW, Seattle, WA, 98107",
#                    "1000 NE Northgate Way, Seattle, WA 98125",
#                    "12801 Aurora Ave N, Seattle, WA 98133",
#                    "2901 E Madison St, Seattle, WA 98112"],)
#newmap.showzipcode(98125)
#newmap.save("map.html")

if __name__ == '__main__':
    unittest.main()