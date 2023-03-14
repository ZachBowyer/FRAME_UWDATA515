""" Tests each method in App/app.py
    run via python Unittest.py
    The output messages let you know when specific tests pass
"""
# Ignoring invalid characters or data types as the input is controlled
# by values passed from front end. For instance, a user cannot execute 
# the zip code shortlist file with a value of -2.babbagui for distance,
# this will be handled by the app itself and won't make its way to the
# function call itself

import unittest
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
       
    def test_zip_to_coordinates(self):
        self.assertAlmostEqual(zip_to_coordinates('98158'), (47.4497, -122.3076),3)
        self.assertAlmostEqual(zip_to_coordinates('98133'), (47.4497, -122.3076),3)
        self.assertAlmostEqual(zip_to_coordinates('98105'), (47.4497, -122.3076),3)
    
    def test_zip_code_shortlist(self):
        self.assertAlmostEqual(zip_code_shortlist('98101', 5),  {'98122': 1.8667019034569339, '98112': 3.2485035505192963, '98109': 2.8110348977324002},3)
        self.assertAlmostEqual(zip_code_shortlist('98102', 2.2),{'98122': 1.8667019034569339, '98112': 3.2485035505192963, '98109': 2.8110348977324002},3)
    
    def test_restaurants_shortlist(self):
        acceptable_zips = {'98103': 0.0, '98115': 4.45, '98105': 4.6, '98117': 4.05}
        self.assertEqual(restaurants_shortlist(acceptable_zips).shape, (18, 5))
    
    def test_price_shortlist(self):
        acceptable_zips = {'98103': 0.0, '98115': 4.45, '98105': 4.6, '98117': 4.05}
        filter_restaurants = restaurants_shortlist(acceptable_zips)
        self.assertEqual(price_shortlist(filter_restaurants, 10.0).shape, (15, 5))
    
    def test_score_shortlist(self):
        acceptable_zips = {'98103': 0.0, '98115': 4.45, '98105': 4.6, '98117': 4.05}
        filter_restaurants = restaurants_shortlist(acceptable_zips)
        filter_price = price_shortlist(filter_restaurants, 10.0)
        self.assertEqual(score_shortlist(filter_price, 4.0).shape, (14, 5))
    
    def test_restaurant_category_shortlist(self):
        acceptable_zips = {'98103': 0.0, '98115': 4.45, '98105': 4.6, '98117': 4.05}
        filter_restaurants = restaurants_shortlist(acceptable_zips)
        filter_price = price_shortlist(filter_restaurants, 10.0)
        filter_score = score_shortlist(filter_price, 4.0)
        self.assertEqual(restaurant_category_shortlist(filter_score, 'Pizza').shape, (3, 5))
    
    def test_food_category_shortlist(self):
        acceptable_zips = {'98103': 0.0, '98115': 4.45, '98105': 4.6, '98117': 4.05}
        filter_restaurants = restaurants_shortlist(acceptable_zips)
        filter_price = price_shortlist(filter_restaurants, 10.0)
        filter_score = score_shortlist(filter_price, 4.0)
        filter_rest_category = restaurant_category_shortlist(filter_score, 'Pizza')
        self.assertEqual(food_category_shortlist(filter_rest_category, 'Vegetarian').shape, (1, 5))
