""" 
Tests each method in App/app.py run via python Unittest.py
The output messages let you know when specific tests pass
"""
# Ignoring invalid characters or data types as the input is controlled
# by values passed from front end. For instance, a user cannot execute 
# the zip code shortlist file with a value of -2.babbagui for distance,
# this will be handled by the app itself and won't make its way to the
# function call itself

import sys
import unittest
import folium
sys.path.insert(0, '../App') #Means unit test has to be run from this folder
# (Need this because we don't want to edit everyones PYTHONPATH)
# pylint: disable=wrong-import-position
from app import *


class TestAppModule(unittest.TestCase):
    
    """ Tests each function in fgmap.py that is outside of the fgmap class. 
        In general, each function will be tested with the following:
            Smoke test             (See if it runs)
            Input validation       (Throws error if input is not correct type)
            Output validation      (Throws error if output is not correct type)
            Expected value test    (We know the expected output ahead of time)
            Edge cases             (Could be anything needed)
    """
    ########################################################################################
    
    # test cases for zip_code_shortlist(zipcode, max_distance)

    ########################################################################################

    def test_zip_code_shortlist_smoke(self):
        """See if app.zip_code_shortlist works"""
        shortlist_zip = app.zip_code_shortlist('98105', 2.5)
        self.assertTrue(True)

    def test_zip_code_shortlist_verifyinput(self):
        """ Expected input for app.zip_code_shortlist(): numeric, numeric """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for app.zip_code_shortlist()")
            app.zip_code_shortlist('a98105', 2.5)
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for app.zip_code_shortlist()")
            app.zip_code_shortlist('98105', 'a2.5')

    def test_zip_code_shortlist_verifyoutput(self):
        """ Expected output for app.zip_code_shortlist(): Dictionary """
        shortlist_zip = zip_code_shortlist('98105', 2.5)
        self.assertIsInstance(shortlist_zip, dict, "zip_code_shortlist() did not return a dictionary")
        
    def test_zip_code_shortlist_expectation(self): 
        """ Compare to expected output """
        shortlist_zip = zip_code_shortlist('98105', 2.5)
        expected_shortlist_zip = {'98105': 0.0, '98115': 2.4356064726094417}
        self.assertAlmostEqual(shortlist_zip, expected_shortlist_zip,
                        "zip_code_shortlist() did not return expected value")

    ########################################################################################
    
    # test cases for restaurants_shortlist(acceptable_zips)

    ########################################################################################


    def test_restaurants_shortlist_smoke(self):
        """See if app.restaurants_shortlist() works"""
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        assert restaurants_shortlist(acceptable_zips).shape == (6318, 19)


    def test_restaurants_shortlist_verifyinput(self):
        """ Expected input for app.restaurants_shortlist(): numeric, numeric """
        with self.assertRaises(TypeError):
            print("Non dictionary input error (arg1) properly raised for app.restaurants_shortlist()")
            app.restaurants_shortlist('98101')

    def test_restaurants_shortlist_verifyoutput(self):
        """ Expected output for app.restaurants_shortlist(): Dictionary """
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        filter_restaurants = restaurants_shortlist(acceptable_zips)
        self.assertIsInstance(filter_restaurants, dict, "restaurants_shortlist() did not return a dictionary")

    ########################################################################################
    
    # test cases for price_shortlist(filter_restaurants, price)

    ########################################################################################

    def test_price_shortlist_smoke(self):
        """See if app.price_shortlist() works"""
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        assert price_shortlist(acceptable_zips).shape == (6318, 19)

    def test_price_shortlist_verifyinput(self):
        """ Expected input for app.zip_code_shortlist(): numeric, numeric """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for app.zip_code_shortlist()")
            app.zip_code_shortlist('a98105', 2.5)
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for app.zip_code_shortlist()")
            app.zip_code_shortlist('98105', 'a2.5')

    def test_price_shortlist_verifyoutput(self):
        """ Expected output for app.price_shortlist(): Dictionary """
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        filter_restaurants = price_shortlist(acceptable_zips)
        self.assertIsInstance(filter_restaurants, dict, "price_shortlist() did not return a dictionary")

    #######################################################################################
    
    # test cases for score_shortlist(filter_price, minimum_rating)

    ########################################################################################

    def test_score_shortlist_smoke(self):
        """See if app.score_shortlist() works"""
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        assert score_shortlist(acceptable_zips).shape == (6318, 19)
        
    def test_score_shortlist_verifyinput(self):
        """ Expected input for app.score_shortlist(): numeric, numeric """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for app.score_shortlist()")
            app.score_shortlist('a98105', 2.5)
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for app.score_shortlist()")
            app.score_shortlist('98105', 'a2.5')

    def test_score_shortlist_verifyoutput(self):
        """ Expected output for app.score_shortlist(): Dictionary """
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        filter_restaurants = score_shortlist(acceptable_zips)
        self.assertIsInstance(filter_restaurants, dict, "score_shortlist() did not return a dictionary")

    ########################################################################################
    
    # test cases for restaurant_category_shortlist(filter_score, restaurant_category_input)

    ########################################################################################

    def test_restaurant_category_shortlist_smoke(self):
        """See if app.restaurant_category_shortlist() works"""
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        assert restaurant_category_shortlist(acceptable_zips).shape == (6318, 19)
        
    def test_restaurant_category_shortlist_verifyinput(self):
        """ Expected input for app.restaurant_category_shortlist(): dataframe, string """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for app.restaurant_category_shortlist()")
            app.restaurant_category_shortlist('a98105', 2.5)
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for app.restaurant_category_shortlist()")
            app.restaurant_category_shortlist('98105', 'a2.5')

    def test_restaurant_category_shortlist_verifyoutput(self):
        """ Expected output for app.restaurant_category_shortlist(): Dictionary """
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        filter_restaurants = restaurant_category_shortlist(acceptable_zips)
        self.assertIsInstance(filter_restaurants, dict, "restaurant_category_shortlist() did not return a dictionary")


    ########################################################################################
    
    # test cases for food_category_shortlist(filter_rest_category, food_category)

    ########################################################################################

    def test_food_category_shortlist_smoke(self):
        """See if app.food_category_shortlist() works"""
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        assert food_category_shortlist(acceptable_zips).shape == (6318, 19)
        
    def test_food_category_shortlist_verifyinput(self):
        """ Expected input for app.food_category_shortlist(): dataframe, string """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for app.food_category_shortlist()")
            app.food_category_shortlist('a98105', 2.5)
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for app.food_category_shortlist()")
            app.food_category_shortlist('98105', 'a2.5')

    def test_food_category_shortlist_verifyoutput(self):
        """ Expected output for app.food_category_shortlist(): Dictionary """
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        filter_restaurants = food_category_shortlist(acceptable_zips)
        self.assertIsInstance(filter_restaurants, dict, "food_category_shortlist() did not return a dictionary")

    ########################################################################################
    
    # test cases for health_inspect_shortlist(filter_food, health_inspect_input)

    ########################################################################################

    def test_health_inspect_shortlist_smoke(self):
        """See if app.health_inspect_shortlist() works"""
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        assert health_inspect_shortlist(acceptable_zips).shape == (6318, 19)
        
    def test_health_inspect_shortlist_verifyinput(self):
        """ Expected input for app.health_inspect_shortlist(): dataframe, string """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for app.health_inspect_shortlist()")
            app.health_inspect_shortlist('a98105', 2.5)
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for app.health_inspect_shortlist()")
            app.health_inspect_shortlist('98105', 'a2.5')

    def test_health_inspect_shortlist_verifyoutput(self):
        """ Expected output for app.health_inspect_shortlist(): Dictionary """
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        filter_restaurants = health_inspect_shortlist(acceptable_zips)
        self.assertIsInstance(filter_restaurants, dict, "health_inspect_shortlist() did not return a dictionary")

    ########################################################################################
    
    # test cases for seating_shortlist(health_inspection_filter, seating_input)

    ########################################################################################

    def test_seating_shortlist_smoke(self):
        """See if app.seating_shortlist() works"""
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        assert seating_shortlist(acceptable_zips).shape == (6318, 19)
        
    def test_seating_shortlist_verifyinput(self):
        """ Expected input for app.seating_shortlist(): dataframe, string """
        with self.assertRaises(ValueError):
            print("Non string input error (arg1) properly raised for app.seating_shortlist()")
            app.seating_shortlist('a98105', 2.5)
        with self.assertRaises(ValueError):
            print("Non string input error (arg2) properly raised for app.seating_shortlist()")
            app.seating_shortlist('98105', 'a2.5')

    def test_seating_shortlist_verifyoutput(self):
        """ Expected output for app.seating_shortlist(): Dictionary """
        acceptable_zips = {'98101': 0.0, '98102': 1.44, '98104': 0.77}
        filter_restaurants = seating_shortlist(acceptable_zips)
        self.assertIsInstance(filter_restaurants, dict, "seating_shortlist() did not return a dictionary")

    ########################################################################################
    
    # test cases for recommend_food(health_inspection_filter, seating_input)

    ########################################################################################

    