# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 14:47:58 2023

@author: adith
"""
import pandas as pd


df = pd.read_csv('Datafordashboard.csv')


#menu = df['Menuitemcategory'].unique()
#menu_categories = {}

#for item in menu:
#    category = item.split(' ')[0]
#    if category in menu_categories:
#        menu_categories[category].append(item)
#    else:
#        menu_categories[category] = [item]

#print(menu_categories)
#print(len(menu_categories))


# Define the mappings between category keywords and main categories
category_mappings = {
    'Starters': 'Appetizers',
    'Vegetarian': 'Entrees',
    'Entrees': 'Entrees',
    'Desserts': 'Desserts',
    'Beverages': 'Drinks',
    'Sides': 'Sides',
    'Salads': 'Salads',
    'Plates': 'Entrees',
    'Sandwiches': 'Sandwiches',
    'Appetizers': 'Appetizers',
    'Platters': 'Entrees',
    'Dessert': 'Desserts',
    'Nachos': 'Entrees',
    'Tacos': 'Entrees',
    'Bowls': 'Entrees',
    'Curried': 'Entrees',
    'Drinks': 'Drinks',
    'Roti': 'Entrees',
    'Teas': 'Drinks',
    'Ice Cream': 'Desserts',
    'Specialties': 'Entrees',
    'Coffee': 'Drinks',
    'Snacks': 'Desserts',
}

# Example data
menu_items = df['Menuitemcategory'].unique()

# Group the menu items by main categories
menu_categories = {}
for item in menu_items:
    # Search for category keywords in the item name
    for category, main_category in category_mappings.items():
        if category in item:
            # Assign the item to the corresponding main category
            if main_category in menu_categories:
                menu_categories[main_category].append(item)
            else:
                menu_categories[main_category] = [item]


import csv
with open('menu_categories.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Category', 'Item'])
    for category, items in menu_categories.items():
        for item in items:
            writer.writerow([category, item])
