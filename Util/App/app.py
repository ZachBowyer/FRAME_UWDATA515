# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 18:37:10 2023

@author: arjun
"""

# Importing Libraries

import numpy as np
import pandas as pd
import streamlit as st
import pgeocode
#data = pd.read_csv('car_dataset.csv')

def zip_to_coordinates(zip_code):
    country = pgeocode.Nominatim('US')
    lat, long = country.query_postal_code(zip_code).latitude, country.query_postal_code(zip_code).longitude
    return lat, long

def recommend_food(zip_input, max_dist_input, allergy_input, diet_input, price_input, misc_input, rating_input):
    latitude, longitude = zip_to_coordinates(zip_input)
    return 

def main():
    
    st.title("FRAME - Food Recommendations for All Methodical Eaters")
    html_temp = """
    <div style = 'background-color: tomato; padding: 60px>
    <h3 style = 'color: white; text-align: center;'></h3>
    <h3 style = 'color: white; text-align: center;'>Hungry but don't know what you want?</h3>
    <h3 style = 'color: white; text-align: center;'>Enter your preferences below, get recommendations!</h3>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    
    st.subheader("")
    st.text_input("Enter your Name: ", 'John Smith', key="name")


    st.subheader("Please enter the required information below.")
    
    # Enter the km driven value
    zipcode = st.text_input('Enter your zip code:', '00000')
    zip_input = zipcode
    # Input for fuel type
    max_distance_limit = st.text_input('Enter your maximum distance preference (miles): ', '0.0')
    max_dist_input = max_distance_limit

    # Input for transmission
    allergies = st.multiselect('Any Allergies?', options = ['Dairy', 'Eggs', 'Gluten', 'Milk', 'Fish', 'Peanuts', 'Tree Nuts', "Other"])
    if "Other" in allergies: 
        allergies = st.text_input("Enter your other option...")
    allergy_input = allergies
    

    # Input for owner
    diet_preference = st.radio('Enter if you have any dietary preferences: ', options = ['Vegetarian', 'Vegan', 'None', 'Other'])
    
    if diet_preference == "Other": 
        diet_preference = st.text_input("Enter your other option...")
        
    diet_input = diet_preference

    # Input for mileage
    price_range = st.slider('Enter your preferred price range: ', 0, 150, (25, 75))
    
    price_input = price_range

    # Input for Age
    misc_preference = st.multiselect('Miscelleaneous Preferences: ', options = ['Low Sodium', 'Keto-Friendly', 'High-Protein', 'Low Fat', 'Other'])
    if "Other" in misc_preference: 
        misc_preference = st.text_input("Enter your other option...")
    misc_input = misc_preference
    
    # Input for seller type
    rating_preference = st.selectbox('Enter restaurant rating preferences (on a scale of 5): ', options=['★ & Up', '★★ & Up', '★★★ & Up', '★★★★ & Up', 'None'])

    rating_input = rating_preference

    result = ''

    if st.button('Get FRAMEd!'):
        result = recommend_food(zip_input, max_dist_input, allergy_input, diet_input, price_input, misc_input, rating_input)
        st.success("Success! We've got some delicious recommendations for you!")
        display_map()
        st.write(f'Thank you {st.session_state.name}! We hope you enjoyed using FRAME!')

def display_map():
    df = pd.DataFrame(
    np.random.randn(5,1)/100 + [47.6062, -122.332],
    columns=['lat', 'lon'])

    st.map(df)    

if __name__ == '__main__':
    main()