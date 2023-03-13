"""
This file is the script that renders the web app written with streamlit for FRAME.
The app is written tailored to the dummy data we have in possession before
developing the app for the entire city of Seattle.
"""
 
# Importing Libraries
import pandas as pd
import streamlit as st
import pgeocode #Temporary need to make it proper module import at some point
from fgmap import fgmap # pylint: disable=import-error, wrong-import-position

# Setting Page configuration
st.set_page_config(
    page_title="FRAME - Food Recommendation for All Methodical Eaters",
    page_icon="🍴", layout = 'wide', initial_sidebar_state="expanded"
)
# Reading the data
df = pd.read_csv("https://raw.githubusercontent.com/Arjun-SC31/DATA-515-Demo/main/App/Food_and_Restaurant_Data.csv")
df['zip_code'] = df['zip_code'].apply(str) # pgeocodes accepts string inputs for zip codes
df_categories = pd.read_csv("https://raw.githubusercontent.com/Arjun-SC31/DATA-515-Demo/main/App/Category_Mapping.csv")
seattle_zips = ['98103', '98122', '98105', '98133', '98107', '98117', '98115',
   '98199', '98112', '98125', '98109', '98155', '98102', '98119',
   '98104', '98177', '98101', '98148', '98166', '98188', '98146',
   '98106', '98134', '98198', '98108', '98118', '98136', '98168',
   '98116', '98126', '98158', '98144', '98121']
def zip_to_coordinates(zip_code):
    '''
    Description: Converts the input zipcode to latitude and longitude coordinates.
    ----------
    Input: zip_code (str) - The user's zip code.
    Returns: lat, long - coordinates corresponding to the user's location
    '''
    country = pgeocode.Nominatim('US')
    lat, long = (country.query_postal_code(zip_code).latitude,
                 country.query_postal_code(zip_code).longitude)
    return lat, long
def zip_code_shortlist(zipcode, max_distance):
    '''
    Description: Returns a dictionary containing the zipcodes within the distance limit, and
    their distance from the customer.
    ----------
    Inputs:
    zipcode: Input zipcode from the user
    max_distance: maximum distance limit from user
    Output:
    dictionary of shortlisted zipcodes.
    Keys: Zipcodes
    Values: Distance of a given zipcode from the user's zipcode.
    '''
    dist_calc = pgeocode.GeoDistance('us')
    # Dictionary containing the shortlisted zipcodes, and their distance from the customer
    shortlist_zip = {}
    for i in seattle_zips:
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
    Description: Shortlists restaurants based on whether the
    restaurant zipcode is present in the list of shortlisted zipcodes.
    ----------
    Input:
    acceptable zips: the dictionary containing the acceptable zip codes and
    distance to user
    Output:
    List of restaurants with acceptable zip codes.
    '''
    filter_restaurants = df[df['zip_code'].isin(acceptable_zips.keys())]
    #st.write('restaurant_shortlist: ', filter_restaurants.shape)
    return filter_restaurants
def price_shortlist(filter_restaurants, price):
    '''
    Description: Returns a filtered dataframe with all dishes
    that cost below a certain price.
    ----------
    Input:
    filter_restaurants: The dataframe with the filtered restaurants previously
    filtered based on distance
    price: The maximum price that the user is willing to pay
    Output:
    filtered dataframe of dishes which cost less than or equal to price.
    '''
    filter_price = filter_restaurants[filter_restaurants['price'] <= price]
    #st.write('price_shortlist: ', filter_price.shape)
    return filter_price
def score_shortlist(filter_price, minimum_rating):
    '''
    Description: Filtering the price-filtered data to only include restaurants
    with a score greater than or equal to the minimum score input by the user
    from '0' to '5'
    ----------
    Input:
    filter_price: obtained dishes after filtering for price
    minimum_rating: lowest acceptable score for a restaurant
    Output:
    filtered dataframe of dishes where the restaurant score is higher
    than the specified minimum.
    '''
    filter_score = filter_price[filter_price['RestaurantScore'] >= minimum_rating]
    #st.write('score_shortlist: ', filter_score.shape)
    return filter_score
def restaurant_category_shortlist(filter_score, restaurant_category_input):
    '''
    Description: Filtering the score-filtered data to only include restaurants
    which match the restaurant category input given by the user.
    ----------
    Input:
    filter_score: obtained dishes after filtering restaurant score
    restaurant_category_input: Desired restaurant category from the user
    Output:
    filtered dataframe of dishes where the restaurant category matches the
    user input.
    '''
    
    rest_category = df_categories[
        df_categories['Updated Category'].str.contains(
            restaurant_category_input
            )
        ]
    list_rest_category = rest_category.RestaurantCategory.values.tolist()
    #st.write(list_rest_category)
    filter_score['result'] = filter_score['RestaurantCategory'].str.contains('|'.join(list_rest_category))
    filter_rest_category = filter_score[filter_score['result'] == True]
    filter_rest_category.drop('result', axis = 1, inplace = True)
    #st.write(filter_rest_category.shape)
    return filter_rest_category
def food_category_shortlist(filter_rest_category, food_category):
    '''
    Description: Filtering the data obtained after filtering restaurant
    categories. The data is further filtered to accommodate food item categories
    ----------
    Input:
    filter_rest_category: obtained dishes after filtering restaurant category
    food_category: Desired food item category
    Output:
    filtered dataframe of dishes where the food item category matches the
    user's desired food item category.
    '''
    filter_food = filter_rest_category[
        filter_rest_category['Category'].str.contains(
            food_category
            )
        ]
    #st.write('food_category_shortlist: ', filter_food.shape)
    return filter_food

def health_inspect_shortlist(filter_food, health_inspect_input):
    '''
    Description: Filtering the data based on user's health inspection preferences.
    ----------
    Input:
    filter_food: Dishes obtained after filtering the food item categories
    health_inspect_input: Health inspection results option taken from user.
    Output:
    filtered dataframe of dishes where the food item category matches the
    user's health inspection requirement.
    '''
    health_results = ['Satisfactory', 'Complete']
    if health_inspect_input == "I'm very particular about health inspections.":
        health_inspection_df = filter_food[
            filter_food['Inspection Result'].isin(health_results)
            ]
    else:
        #st.write('health_inspect_shortlist_dont_care: ', filter_food.shape)
        return filter_food
    #st.write('health_inspect_shortlist_care: ', health_inspection_df.shape)
    return health_inspection_df
def recommend_food(zip_input, max_dist_input, restaurant_category_input,
                   diet_input, price_input,rating_input, health_inspection_input):
    # pylint: disable=too-many-arguments
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
    if zip_input not in seattle_zips:
        st.error('Invalid zipcode, please try again!', icon="🚨")
        st.stop()
    # Filtering restaurants based on acceptable zipcodes
    filter_restaurants = restaurants_shortlist(zip_dict)
    # Filtering dishes to within the price limit
    filter_price = price_shortlist(filter_restaurants, price_input)
    # Filtering dishes based on restaurant score
    filter_score = score_shortlist(filter_price, rating_input)
    # Cuisine based filtering
    filter_cuisine = restaurant_category_shortlist(filter_score,
                                                   restaurant_category_input)
    # filter based on dietary preferences
    filter_food_category = food_category_shortlist(filter_cuisine, diet_input)
    filter_food_category = filter_food_category.sort_values(by = ['RestaurantScore'],
                                          ascending = False)
    health_inspection_filter = health_inspect_shortlist(filter_food_category,
                                                        health_inspection_input)
    return health_inspection_filter.head()
def main():
    # pylint: disable=too-many-locals
    '''
    The web app is rendered through this function.
    User inputs taken through this function.
    '''
    st.markdown("<h1 style='text-align: center; color: white;'>FRAME - Food Recommendations for All Methodical Eaters 🍴</h1>", unsafe_allow_html=True)
    #st.title("FRAME - Food Recommendations for All Methodical Eaters 🍴")
    placeholder = st.empty()
    with placeholder.form("FRAME_form"):
        st.subheader("Enter your preferences:")
        # Input for user zipcode and max distance
        left_zip, right_dist = st.columns(2)
        zip_input = left_zip.text_input('Zip code:', '98105')
        # Input for maximum distance from user
        max_dist_input = right_dist.number_input('Maximum distance preference (miles): ', 0.5)
        # Input for cuisine and diet restrictions
        left_restaurants, right_food = st.columns(2)
        restaurant_category = ['Other','African', 'American', 'Asian', 'Bakery', 'Breakfast',
                                 'Cafe', 'Chinese', 'Comfort Food', 'Desserts', 'European',
                                 'Healthy', 'Indian', 'Italian', 'Japanese', 'Korean',
                                 'Mediterranean', 'Mexican','Middle Eastern', 'Pizza',
                                 'Seafood', 'Thai', 'Vegan', 'Vegetarian', 'Vietnamese']
        restaurant_category_input = left_restaurants.selectbox('Restaurant Category:',
                                                               options = restaurant_category)
        # Input for dietary preferences
        food_item_category = ['Other', 'Appetizers', 'Entrees', 'Beverages',
                              'Sides', 'Salads', 'Platters', 'Desserts', 'Snacks']
        food_category_input = right_food.selectbox('Food Category',
                                                   options = food_item_category)
        # Input for price range and rating preference
        left_price, right_rating = st.columns(2)
        price_input = left_price.slider('Maximum Price ($): ', 0.0, 250.0, 1.0)
        # Input for restaurant rating preferences
        rating_input = right_rating.slider('Minimum acceptable restaurant score: ', 0.0, 5.0, 1.0)
        # Input for restaurant health inspection
        health_inspect_input = st.selectbox('Inspection Results: ',
                                            options = [
                                                "Doesn't matter, food is food!",
                                                "I'm very particular about health inspections."
                                                                             ])
        submit = st.form_submit_button("Get FRAMEd!")
    if submit:
        final_filter = recommend_food(zip_input, max_dist_input,
                                      restaurant_category_input, food_category_input,
                                      price_input, rating_input, health_inspect_input)
        if len(final_filter.index) == 0:
            st.error(
                "Sorry, we couldn't find any recommendations for the given criteria!",
                icon="😞")
            st.stop()
        else:
            pass
        placeholder.empty()
        st.balloons()
        st.header('Below are your food recommendations:')
        #st.write(final_filter.shape)
        restaurants = []
        
        g_map, food_recommendations = st.columns([5,4], gap="large")
        with g_map:
            for i in range (1,len(final_filter.index)+1):
                innerlist = []
                innerlist.append(final_filter.iloc[i-1,-3])
                innerlist.append(final_filter.iloc[i-1,1])
                innerlist.append(final_filter.iloc[i-1,6])
                restaurants.append(innerlist)
            st.markdown(
                "<h3 style='text-align: left;'>View Map for more insight</h3>",
                unsafe_allow_html=True
                )
            display_map(restaurants, int(zip_input))
        with food_recommendations:
            for i in range (1,len(final_filter.index)+1):
                st.subheader(f'#{i}: {final_filter.iloc[i-1,11]}')
                st.text(f'Restaurant: {final_filter.iloc[i-1,1]}')
                st.text(f'Price: ${final_filter.iloc[i-1,-2]}')
                st.text(f'Description: {final_filter.iloc[i-1,-3]}')
                st.text(f'Restaurant Address: {final_filter.iloc[i-1,6]}')
                #st.text(" ")
            #final_filter
        st.success('Thank you! We hope you enjoyed using FRAME!')
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col3:
            try_again = st.button("Get FRAMEd (Again)")
            if try_again:
                main()
        with col4:
            pass
        with col5:
            pass
        
def display_map(restaurants, zip_input):
    '''
    Displays the restaurants suggested as well as the user's input location
    on a map embedded into the web page.
    '''
    newmap = fgmap.Fgmap()
    newmap.createmap(origin=str(zip_input))
    #Draw trip line and add point at each restaurant
    index = 0
    for restaurant in restaurants:
        #description = restaurant[0]
        name = restaurant[1]
        address = restaurant[2]
        newmap.addtrippolyline(address, color=newmap.colors[index])
        newmap.addmarker(address, popup=name, icon="star", color=newmap.colors[index])
        index += 1
    newmap.showzipcode(zip_input)
    htmlstring = newmap.returnhtml()
    st.components.v1.html(htmlstring, width=700, height=1000, scrolling=True)
    #How to get address distances
    #distances = []
    #for address in restaurants:
    #    distance = getdistanceoftrip(originAddress, address)
    #    duration = getdurationoftrip(originAddress, address)
        #Return string: "50 miles" #str.split()
if __name__ == '__main__':
    main()
