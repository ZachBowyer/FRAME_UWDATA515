"""
This file is the script that renders the web app written with streamlit for FRAME.
The app is written tailored to the dummy data we have in possession before
developing the app for the entire city of Seattle.
"""

# Importing Libraries
import numpy as np
import pandas as pd
import streamlit as st
import pgeocode
import sys
sys.path.insert(0, '../../../fgmap') #Temporary need to make it proper module import at some point
import fgmap 
# Setting Page configuration

st.set_page_config(
    page_title="FRAME - Food Recommendation for Methodical Eaters", 
    page_icon="🍴", initial_sidebar_state="expanded"
)

# Reading the data
df = pd.read_csv("sampledata515.csv", encoding = "utf-8", encoding_errors = 'ignore')
df['Zip'] = df['Zip'].apply(str) # pgeocodes accepts string inputs for zip codes
    
def zip_to_coordinates(zip_code):
    '''
    Converts the input zipcode to latitude and longitude coordinates.
    '''
    country = pgeocode.Nominatim('US')
    lat, long = country.query_postal_code(zip_code).latitude, country.query_postal_code(zip_code).longitude
    return lat, long

def zip_code_shortlist(zipcode, max_distance):
    '''
    zipcode: Input zipcode from the user
    max_distance: maximum distance limit from user
    
    Returns a dictionary containing the zipcodes within the distance limit, and
    their distance from the customer.
    '''
    dist_calc = pgeocode.GeoDistance('us')
    # Dictionary containing the shortlisted zipcodes, and their distance from the customer
    shortlist_zip = {}
    for i in df['Zip']:
        distance = dist_calc.query_postal_code(zipcode, str(i))
    
        if float(distance) <= float(max_distance):
            if str(i) not in shortlist_zip:
                shortlist_zip[str(i)] = distance
            else:
                pass
        else:
            pass
    # Dictionary returned to the recommend_food function
    return shortlist_zip
    
def restaurants_shortlist(acceptable_zips):
    '''
    acceptable zips: the dictionary containing the acceptable zip codes and 
    distance to source
    
    Filters the dataset based on acceptable distance
    '''
    filter_restaurants = df[df['Zip'].isin(acceptable_zips.keys())]
    
    return filter_restaurants
    
def price_shortlist(filter_restaurants, price):
    '''
    filter_restaurants: The dataframe with the filtered restaurants previously
    filtered based on distance
    
    Returns a filtered dataframe with all dishes that cost below a certain price.
    '''
    filter_price = filter_restaurants[filter_restaurants['Actual Price'] <= price]
    
    return filter_price

def score_shortlist(filter_price, minimum_rating):
    '''
    filter price: obtained dishes after filtering for price
    minimum rating: lowest acceptable score for a restaurant
    
    Filtering the price-filtered data to only include restaurants with a score
    greater than or equal to the minimum allowance.
    '''
    filter_score = filter_price[filter_price['Score'] >= minimum_rating]
    
    return filter_score

def cuisine_shortlist(filter_score, cuisine_input):
    '''
    '''
    filter_cuisine = filter_score[filter_score['Category'].str.contains(cuisine_input)]
    
    return filter_cuisine

def diet_shortlist(filter_cuisine, diet_input):
    '''
    '''
    filter_diet = filter_cuisine[filter_cuisine['Category'].str.contains(diet_input)]
    
    return filter_diet

def recommend_food(zip_input, max_dist_input, cuisine_input, diet_input, price_input,rating_input):
    '''
    Takes the user responses as input to then filter restaurant and dishes data 
    such that the dishes most closely matching user requirements are selected.
    
    1. filter based on distance parameter - done
    2. filter based on price range - done
    3. filter based on restaurant score - done
    4. Fuzzy Matching based on cuisine
    5. fuzzy matching based on dietary preferences
    '''
    # Getting the zipcodes within acceptable distance
    zip_dict = zip_code_shortlist(str(zip_input), max_dist_input)
    
    # Filtering restaurants based on acceptable zipcodes
    filter_restaurants = restaurants_shortlist(zip_dict)
    
    # Filtering dishes to within the price limit
    filter_price = price_shortlist(filter_restaurants, price_input)
    
    # Filtering dishes based on restaurant score
    filter_score = score_shortlist(filter_price, rating_input)
    
    # Cuisine based filtering
    filter_cuisine = cuisine_shortlist(filter_score, cuisine_input)
    
    # filter based on dietary preferences
    filter_diet = diet_shortlist(filter_cuisine, diet_input)
    
    filter_diet = filter_diet.sort_values(by = ['Score'], ascending = False)
    return filter_diet.head()

def main():
    '''
    The web app is rendered through this function. 
    User inputs taken through this function.
    '''
    st.title("FRAME - Food Recommendations for All Methodical Eaters 🍴")
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

    # Input for cuisine
    
    cuisine = st.radio('Choose Cuisine:', options = ['Greek', 'Mediterranean',
                                                       'American', 'Italian', 'Pizza',
                                                       'Mexican', 'Latin American', 'New Mexican'])
        
    cuisine_input = cuisine
    

    # Input for dietary preferences
    diet_preference = st.radio('Enter if you have any dietary preferences: ', options = ['Vegetarian Friendly',
                                                                                         'Gluten Free Friendly',
                                                                                         'Allergy Friendly', 'None', 'Other'])
    
    
    if diet_preference == 'None':
        diet_preference = ''
    
    diet_input = diet_preference
    
    # Input for price range
    price_range = st.slider('Enter maximum price limit: ', 0, 50, 1)
    
    price_input = price_range
    
    # Input for restaurant rating preferences
    rating_preference = st.slider('Enter minimum acceptable restaurant score: ', 4.0, 15.0, 4.5)

    rating_input = rating_preference


    if st.button('Get FRAMEd!'):
        final_filter = recommend_food(zip_input, max_dist_input, cuisine_input, diet_input, price_input, rating_input)
        st.header('Below are your food recommendations:')
        st.subheader("")
        
        restaurants = []
        for i in range (1,6):
            st.subheader(f'#{i}: {final_filter.iloc[i-1,11]}   _(${final_filter.iloc[i-1,-2]})_')
            st.text(f'Description: {final_filter.iloc[i-1,-3]}')
            st.text(f'From: {final_filter.iloc[i-1,2]}')
            st.text(f'Restaurant Address: {final_filter.iloc[i-1,6]}')
            innerlist = []
            innerlist.append(final_filter.iloc[i-1,-3])
            innerlist.append(final_filter.iloc[i-1,2])
            innerlist.append(final_filter.iloc[i-1,6])
            restaurants.append(innerlist)
            st.header(" ")
        #final_filter
        display_map(restaurants, zip_input)
        st.success(f'Thank you {st.session_state.name}! We hope you enjoyed using FRAME!')

def display_map(restaurants, zip_input):
    '''
    Displays the restaurants suggested as well as the user's input location 
    on a map embedded into the web page.
    '''
    newmap = fgmap.Fgmap()
    newmap.createmap(origin=zip_input)

    #Draw trip line and add point at each restaurant 
    index = 0
    for restaurant in restaurants:
        description = restaurant[0]
        name = restaurant[1]
        address = restaurant[2]
        newmap.addtrippolyline(address, color=newmap.colors[index])
        newmap.addmarker(address, popup=name, icon="star", color=newmap.colors[index])
        index += 1
    
    newmap.showzipcode(zip_input)
    htmlstring = newmap.returnhtml()
    st.components.v1.html(htmlstring, width=700, height=700, scrolling=True)  
    
    #How to get address distances
    #distances = []
    #for address in restaurants:
    #    distance = getdistanceoftrip(originAddress, address)
    #    duration = getdurationoftrip(originAddress, address)
        #Return string: "50 miles" #str.split()

if __name__ == '__main__':
    main()