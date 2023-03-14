# -*- coding: utf-8 -*-
"""
This code reads in 3 datasets: KingCounty Inspection data (seagov.csv),
UberEats restaurant (restaurants.csv) & menu data (restaurant-menus.csv),
filters them based on zip code and performs a fuzzy match algorithm using
the address column to merge restaurant data with KingCounty Inspection data.
It then merges the resulting dataset with menu data and applies a regular
expression pattern to clean the restaurant name and dish name columns.
Finally, it saves the updated dataset to a new file. The resulting dataset is
intended for use in the frontend dashboard.
"""

import re
import warnings
import pandas as pd
from fuzzywuzzy import fuzz, process
warnings.filterwarnings("ignore")

# Define a regular expression pattern to match each category
PATTERNS = {
    'Appetizers': r'\b(Appetizers|Starters|Mezze|Fries|Nuggets)\b',
    'Entrees': r'\b(Breakfast|Dinner|Lunch|Entrees|Plates|Burritos|Tacos|Bowls|Pasta|'
               r'Burger|Biryani|Curries|Pizza|Pizzas|Indian)\b',
    'Beverages': r'\b(Beverages|Drinks|Teas|Shakes|Coffee|Coffees|Beverage)\b',
    'Sides': r'\b(Side Orders|Sides|Combo Sides|Contorni|Condiments|Sides)\b',
    'Salads': r'\b(Salads)\b',
    'Platters': r'\b(Platters|Plate)\b',
    'Desserts': r'\b(Desserts|Ice Cream|Pies|Cupcakes|Bake at Home|Dessert|Yogurt|Bakery)\b',
    'Snacks': r'\b(Snacks|Savory Pies|Cookies|Snack)\b',
    'Other': r'.*'
}

# Define the mapping data as a list of tuples
mapping_data = [
    ('Seating 0-12 - Risk Category III', '0 - 12'),
    ('Seating 13-50 - Risk Category III', '13 - 50'),
    ('Seating 51-150 - Risk Category III', '51 - 150'),
    ('Bakery-no seating - Risk Category II', 'No Seating'),
    ('Grocery Store-no seating - Risk Category I', 'No Seating'),
    ('Seating > 250 - Risk Category III', '> 250'),
    ('Seating 151-250 - Risk Category III', '151-250'),
    ('Seating 13-50 - Risk Category II', '13 - 50'),
    ('Caterer - Risk Category II', 'No Seating'),
    ('Mobile Food Unit - Risk Category III', 'No Seating'),
    ('Caterer - Risk Category III', 'No Seating'),
    ('Seating 13-50 - Risk Category I', '13 - 50'),
    ('Seating 0-12 - Risk Category I', '0 - 12'),
    ('Meat/Sea Food - Risk Category III', 'No Seating'),
    ('Bakery-no seating - Risk Category III', 'No Seating'),
    ('Seating 0-12 - Risk Category II', '0 - 12'),
    ('Caterer - Risk Category I', 'No Seating'),
    ('Limited Food Services - no permanent plumbing', 'No Seating'),
    ('Seating 51-150 - Risk Category I', '51 - 150'),
    ('Seating 51-150 - Risk Category II', '51 - 150'),
    ('School Lunch Program - Risk II', 'No Seating'),
    ('Mobile Food Unit - Risk Category I', 'No Seating'),
    ('Mobile Food Unit - Risk Category II', 'No Seating'),
    ('Non-Profit Institution - Risk Category III', 'No Seating'),
    ('Grocery Store-no seating - Risk Category II', 'No Seating'),
    ('Bakery-no seating - Risk Category I', 'No Seating'),
    ('Seating > 250 - Risk Category I', '> 250'),
    ('Non-Profit Institution - Risk Category II', 'No Seating'),
    ('Non-Profit Institution - Risk Category I', 'No Seating'),
    ('Seating 151-250 - Risk Category I', '151-250'),
    ('Seating > 250 - Risk Category II', '> 250'),
    ('Bed and Breakfast - Risk Category I', 'No Seating'),
    ('Seating 151-250 - Risk Category II', '151-250')
]

#def map_category(category):
#    """
#    Maps a given category string to a predefined category key using regular expressions.
#    Args:
#        category (str): A string representing the category to be mapped.
#    Returns:
#        str: A category key that matches the given category string based on
#            predefined regular expression patterns.
#             If no matching pattern is found, returns None.
#    Raises:
#        None.
#    """
#    for key, pattern in PATTERNS.items():
#        if re.search(pattern, category, re.IGNORECASE):
#            return key

# Create a function to map each category using the regex patterns
def map_category(category):
    """
    Maps a given category string to a predefined category key using regular expressions.
    Args:
        category (str): A string representing the category to be mapped.
    Returns:
        str: A category key that matches the given category string based on
            predefined regular expression patterns.
             If no matching pattern is found, returns None.
    Raises:
        None.
    """
    result = None
    for key, pattern in PATTERNS.items():
        if re.search(pattern, category, re.IGNORECASE):
            result = key
            break
    return result


# Cleaning of KingCounty Inspection data
king_data = pd.read_csv('../../data/seagov.csv')
king_data['Date'] = pd.to_datetime(king_data['Inspection Date']).dt.strftime('%Y/%m/%d')

# Taking the latest record for every retaurant
king_data_df = king_data.sort_values('Date').groupby(['Name','Address']).tail(1)

# Reading Ubereats data
rest = pd.read_csv('../../data/restaurants.csv')
menu = pd.read_csv('../../data/restaurant-menus.csv')

# Filtering for restaurants only in Seattle area
rest_sea= rest[rest['zip_code'].str.startswith('981', na=False)]


# To merge Inspection data with Uber eats restaurant data,
# we will use the address column and perform a fuzzy match algorithm
# as we do not have 2 coulmns that are identical to do a pd.merge()

king_data_df["FA"] = king_data_df["Address"] + ' ' + king_data_df["City"] + ' '
king_data_df["FA"] += king_data_df["Zip Code"].astype(str)

king_data_df = king_data_df[['Name','FA','Inspection Result','Grade','Description']]

# Replace blanks with "No rating"
king_data_df['Grade'].fillna('Unrated', inplace=True)
king_data_df['Grade'].replace('', 'Unrated', inplace=True)

# Replace 1 with "Excellent"
king_data_df['Grade'].replace(1, 'Excellent', inplace=True)

# Replace 2 with "Good"
king_data_df['Grade'].replace(2, 'Good', inplace=True)

# Replace 3 with "Okay"
king_data_df['Grade'].replace(3, 'Okay', inplace=True)

# Replace 4 with "Needs to improve"
king_data_df['Grade'].replace(4, 'Needs to improve', inplace=True)

# Convert the mapping data to a dictionary
description_to_seats = dict(mapping_data)

# Create a new column called "Seats" in the other dataset
king_data_df["Seats"] = king_data_df["Description"].map(description_to_seats)

rest_sea['full_address'] = rest_sea['full_address'].str.lower().str.strip()
king_data_df['FA'] = king_data_df['FA'].str.lower().str.strip()

# Drop NaNs
rest_sea=rest_sea.dropna()
king_data_df=king_data_df.dropna()

# Fuzzy Match (Merge if the score > 80)
THRESHOLD=80
LIMIT=1
matches = []
for row in rest_sea['full_address']:
    match = process.extractOne(row, king_data_df['FA'],
                               scorer=fuzz.token_sort_ratio,
                               score_cutoff=THRESHOLD)
    if match:
        matches.append((row, match[0], match[1]))

matches_df = pd.DataFrame(matches, columns=['match1', 'match2', 'score'])
matches_df = matches_df[matches_df['score'] >= THRESHOLD].sort_values(
    'score', ascending=False).groupby('match1').head(LIMIT)

merged_df = pd.merge(rest_sea, matches_df, left_on= 'full_address', right_on='match1', how='left')
merged_df = pd.merge(merged_df, king_data_df, left_on='match2', right_on='FA', how='left')
merged_df = merged_df.drop(columns=['match1', 'match2', 'score_y','Name','FA'])


# Merge Menu data with restaurant data
front_end_data = pd.merge(merged_df,menu , left_on='id', right_on = 'restaurant_id', how='right')
front_end_data=front_end_data.dropna()
front_end_data = front_end_data.rename(columns={'name_x': 'RestaurantName',
                                                'score_x': 'RestaurantScore',
                                                'category_x': 'RestaurantCategory',
                                                'category_y': 'Menuitemcategory',
                                                'name_y': 'DishName'})
front_end_data = front_end_data.drop(columns=['id','restaurant_id'])

# apply the mapping function to the category column
front_end_data['Category'] = front_end_data['Menuitemcategory'].apply(map_category)


# To clean RestaurantName & DishName column
# define regular expression pattern to match non-alphanumeric characters
pattern_name = re.compile(r'[^a-zA-Z0-9\s]')

# apply regex pattern to RestaurantName column and overwrite original column
front_end_data['RestaurantName'] = front_end_data['RestaurantName'].apply(
    lambda x: re.sub(pattern_name, '', x))
front_end_data['DishName'] = front_end_data['DishName'].apply(lambda x: re.sub(pattern_name, '', x))

# save the updated dataframe to a new file
front_end_data.to_csv('../../data/Datafordashboard.csv', index=False)
print("DATA IS READY!!!")
