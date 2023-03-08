# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:04:20 2023

@author: adithyaa
"""

import pandas as pd

# Cleaning of KingCounty Inspection data
king_data = pd.read_csv('seagov.csv')
king_data['Date'] = pd.to_datetime(king_data['Inspection Date']).dt.strftime('%Y/%m/%d')

# Taking the latest record for every retaurant
king_data_df = king_data.sort_values('Date').groupby(['Name','Address']).tail(1)

# Reading Ubereats data
rest = pd.read_csv('restaurants.csv')
menu = pd.read_csv('restaurant-menus.csv')

# Filtering for restaurants only in Seattle area
rest_sea= rest[rest['zip_code'].str.startswith('981', na=False)]


# To merge Inspection data with Uber eats restaurant data,
# we will use the address column and perform a fuzzy match algorithm 
# as we do not have 2 coulmns that are identical to do a pd.merge()

king_data_df["FA"] = king_data_df["Address"] + ' ' + king_data_df["City"] + ' ' + king_data_df["Zip Code"].astype(str)
king_data_df = king_data_df[['Name','FA','Inspection Result']]

rest_sea['full_address'] = rest_sea['full_address'].str.lower().str.strip()
king_data_df['FA'] = king_data_df['FA'].str.lower().str.strip()

# Drop NaNs
rest_sea=rest_sea.dropna()
king_data_df=king_data_df.dropna()

# Fuzzy Match (Merge if the score > 80)
from fuzzywuzzy import fuzz, process
threshold=80
limit=1
matches = []
for row in rest_sea['full_address']:
    match = process.extractOne(row, king_data_df['FA'], scorer=fuzz.token_sort_ratio, score_cutoff=threshold)
    if match:
        matches.append((row, match[0], match[1]))
        

matches_df = pd.DataFrame(matches, columns=['match1', 'match2', 'score'])
matches_df = matches_df[matches_df['score'] >= threshold].sort_values('score', ascending=False).groupby('match1').head(limit)

merged_df = pd.merge(rest_sea, matches_df, left_on= 'full_address', right_on='match1', how='left')
merged_df = pd.merge(merged_df, king_data_df, left_on='match2', right_on='FA', how='left')
merged_df = merged_df.drop(columns=['match1', 'match2', 'score_y','Name','FA'])


# Merge Menu data with restaurant data
front_end_data = pd.merge(merged_df,menu , left_on='id', right_on = 'restaurant_id', how='right')
front_end_data=front_end_data.dropna()
front_end_data = front_end_data.rename(columns={'name_x': 'RestaurantName', 'score_x': 'RestaurantScore',
                                                'category_x': 'RestaurantCategory', 'category_y': 'Menuitemcategory',
                                                'name_y': 'DishName'})
front_end_data = front_end_data.drop(columns=['id','restaurant_id'])
front_end_data.to_csv('Datafordashboard.csv',index=False)
#front_end_data[front_end_data['id']==7687]

