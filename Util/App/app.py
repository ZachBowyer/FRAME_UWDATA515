"""
This file is the script that renders the web app written with streamlit for FRAME.
"""

# Importing Libraries
import numpy as np
import pandas as pd
import streamlit as st
import pgeocode

def zip_to_coordinates(zip_code):
    '''
    Converts the input zipcode to latitude and longitude coordinates.
    '''
    country = pgeocode.Nominatim('US')
    lat, long = country.query_postal_code(zip_code).latitude, country.query_postal_code(zip_code).longitude
    return lat, long

def recommend_food(zip_input, max_dist_input, allergy_input, diet_input, price_input, misc_input, rating_input):
    '''
    Takes the user responses as input to then filter restaurant and dishes data such that the dishes most closely matching user requirements are selected.
    '''
    latitude, longitude = zip_to_coordinates(zip_input)
    return 

def main():
    '''
    The web app is rendered through this function. User inputs taken through this function.
    '''
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
    
    # Input for user zipcode
    zipcode = st.text_input('Enter your zip code:', '00000')
    zip_input = zipcode
    
    # Input for maximum distance from user
    max_distance_limit = st.text_input('Enter your maximum distance preference (miles): ', '0.0')
    max_dist_input = max_distance_limit

    # Input for allergies
    allergies = st.multiselect('Any Allergies?', options = ['Dairy', 'Eggs', 'Gluten', 'Milk', 'Fish', 'Peanuts', 'Tree Nuts', "Other"])
    if "Other" in allergies: 
        allergies = st.text_input("Enter your other option...")
    allergy_input = allergies
    

    # Input for dietary preferences
    diet_preference = st.radio('Enter if you have any dietary preferences: ', options = ['Vegetarian', 'Vegan', 'None', 'Other'])
    
    if diet_preference == "Other": 
        diet_preference = st.text_input("Enter your other option...")
        
    diet_input = diet_preference

    # Input for price range
    price_range = st.slider('Enter your preferred price range: ', 0, 150, (25, 75))
    
    price_input = price_range

    # Input for miscellaneous preferences
    misc_preference = st.multiselect('Miscelleaneous Preferences: ', options = ['Low Sodium', 'Keto-Friendly', 'High-Protein', 'Low Fat', 'Other'])
    if "Other" in misc_preference: 
        misc_preference = st.text_input("Enter your other option...")
    misc_input = misc_preference
    
    # Input for restaurant rating preferences
    rating_preference = st.selectbox('Enter restaurant rating preferences (on a scale of 5): ', options=['★ & Up', '★★ & Up', '★★★ & Up', '★★★★ & Up', 'None'])

    rating_input = rating_preference

    result = ''

    if st.button('Get FRAMEd!'):
        result = recommend_food(zip_input, max_dist_input, allergy_input, diet_input, price_input, misc_input, rating_input)
        st.success("Success! We've got some delicious recommendations for you!")
        display_map()
        st.write(f'Thank you {st.session_state.name}! We hope you enjoyed using FRAME!')

def display_map():
    '''
    Displays the restaurants suggested as well as the user's input location on a map embedded into the web page.
    '''
    df = pd.DataFrame(
    np.random.randn(5,1)/100 + [47.6062, -122.332],
    columns=['lat', 'lon'])

    st.map(df)    

if __name__ == '__main__':
    main()
