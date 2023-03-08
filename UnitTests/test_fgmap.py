import fgmap 
import unittest

#class TestGoogleMapsMethods(unittest.testcase):
#    def test():
#        x=1
#
#class TestMapMethods(unittest.testcase):
#    def test():
#        x=1
#
#if __name__ == '__main__':
#    unittest.main()

#Tests
newmap = fgmap.Fgmap()
newmap.createmap(origin="4555 Roosevelt Way NE, Seattle, WAS 98105")
test = newmap.returnhtml()
print(test)
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
