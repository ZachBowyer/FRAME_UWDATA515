"""
Test file to get some information about the uber eats kaggle dataset.
Information located on the top level readme.md file also used excel. 
This dataset is located at: 
https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus?resource=download
"""
import pandas as pd

#Load in csvs as dataframes
restaurants = pd.read_csv('../data/UberEats/restaurants.csv')
menus = pd.read_csv('../data/UberEats/restaurant-menus.csv')
#print(restaurants.dtypes)
#print(menus.dtypes)
#print(restaurants.head())
#print(menus.head())

#Get percent of dataset with null values for each column for restaurants data:
for columnName in restaurants.columns.values:
    null_list = restaurants[columnName].isnull()
    COUNTNULL = 0
    COUNTNOTNULL = 0
    for isratingnull in null_list:
        if isratingnull is True:
            COUNTNULL += 1
        else:
            COUNTNOTNULL += 1
    print("For", columnName, COUNTNULL, "/", COUNTNULL+COUNTNOTNULL,
          COUNTNULL/(COUNTNULL+COUNTNOTNULL))

#Get percent of dataset with null values for each column for menus data:
for columnName in menus.columns.values:
    null_list = menus[columnName].isnull()
    COUNTNULL = 0
    COUNTNOTNULL = 0
    for isratingnull in null_list:
        if isratingnull is True:
            COUNTNULL += 1
        else:
            COUNTNOTNULL += 1
    print("For", columnName, COUNTNULL, "/", COUNTNULL+COUNTNOTNULL,
          COUNTNULL/(COUNTNULL+COUNTNOTNULL))

#Get number of restaurants in seattle and number of all combined menu items from those restaurants
# pylint: disable=singleton-comparison
seattle_restaurants = restaurants[restaurants["full_address"].str.contains("Seattle") == True]
MENUITEMSUM = 0
seattle_restaurant_ids = seattle_restaurants['id']
for restaurantid in seattle_restaurant_ids:
    restaurant_menu = menus[menus["restaurant_id"] == restaurantid]
    MENUITEMSUM += len(restaurant_menu)
print("There are", len(seattle_restaurants), "seattle restaurant with", MENUITEMSUM, "menu items")
