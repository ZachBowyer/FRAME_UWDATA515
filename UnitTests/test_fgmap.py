import sys
sys.path.insert(0, '../fgmap')
import fgmap 
import unittest

class TestGoogleMapsMethods(unittest.TestCase):
    def test_getaddresscoordinates_verifyinput(self):
        """
        Make sure getaddresscoordinates() can only take in a string
        """
        with self.assertRaises(ValueError):
            print("Properly raised")
            fgmap.getaddresscoordinates(99338)
    
    def test_getaddresscoordinates_verifyreturn(self):
        """
        Make sure getaddresscoordinates() returns a list with 2 floats
        """
        

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