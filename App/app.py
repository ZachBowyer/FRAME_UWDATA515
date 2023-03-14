"""
This file is the script that renders the web app written with streamlit for FRAME.
The app is written tailored to the dummy data we have in possession before
developing the app for the entire city of Seattle.
"""
# Importing Libraries
import sys
import pandas as pd # pylint: disable=import-error
import streamlit as st # pylint: disable=import-error
import pgeocode # pylint: disable=import-error
sys.path.insert(0, 'fgmap')
from fgmap import fgmap # pylint: disable=import-error, wrong-import-position
# Setting Page configuration
st.set_page_config(
    page_title="FRAME - Food Recommendation for All Methodical Eaters",
    page_icon="🍴", layout = 'wide', initial_sidebar_state="expanded"
)
# Reading the data
df = pd.read_csv("../data/Datafordashboard.csv")
df['zip_code'] = df['zip_code'].apply(str) # pgeocodes accepts string inputs for zip codes
df_categories = pd.read_csv("../data/Category_Mapping.csv")
seattle_zips = ['98101', '98102', '98103', '98104', '98105', '98106', '98107',
'98108', '98109', '98112', '98115', '98116', '98117', '98118', '98119', '98121',
'98122', '98125', '98126', '98133', '98134', '98136', '98144', '98146', '98148',
'98155', '98158', '98166', '98168', '98177', '98188', '98198', '98199']
def zip_code_shortlist(zipcode, max_distance):
    '''
    Description: Returns a dictionary containing the zipcodes within the distance limit, and
    their distance from the customer.
    ----------
    Execution String: zip_code_shortlist('98105', 2.5)
    Inputs:
    zipcode: Input zipcode from the user
    max_distance: maximum distance limit from user
    Output:
    dictionary of shortlisted zipcodes.
    Keys: Zipcodes
    Values: Distance of a given zipcode from the user's zipcode.
    '''
    # Check for valid zipcode format
    if not isinstance(zipcode,str) or len(zipcode) != 5:
        raise ValueError("Invalid zipcode format. Please enter a 5-digit numeric zipcode.")

    # Check for valid maximum distance
    try:
        max_distance = float(max_distance)
        if max_distance <= 0:
            raise ValueError("Maximum distance must be a positive number.")
    except ValueError as exc:
        raise ValueError("Invalid maximum distance. Please enter a valid distance.") from exc

    # Connect to geocoding service
    try:
        dist_calc = pgeocode.GeoDistance('us')
    except ConnectionError as exc:
        raise ConnectionError("Could not connect to geocoding service. Try again.") from exc

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
    Execution String: restaurants_shortlist(shortlist_zip)
    Input:
    acceptable_zips: the dictionary containing the acceptable zip codes and
    distance to user
    Output:
    List of restaurants with acceptable zip codes.
    '''
    # Check for valid input type
    if not isinstance(acceptable_zips, dict):
        raise TypeError("acceptable_zips must be a dictionary.")
    filter_restaurants = df[df['zip_code'].isin(acceptable_zips.keys())]
    #st.write('restaurant_shortlist: ', filter_restaurants.shape)
    return filter_restaurants
def price_shortlist(filter_restaurants, price):
    '''
    Description: Returns a filtered dataframe with all dishes
    that cost below a certain price.
    ----------
    Execution String: price_shortlist(filter_restaurants, price)
    Input:
    filter_restaurants: The dataframe with the filtered restaurants previously
    filtered based on distance
    price: The maximum price that the user is willing to pay
    Output:
    filtered dataframe of d34ishes which cost less than or equal to price.
    '''
    # Check for valid input types
    if not isinstance(filter_restaurants, pd.DataFrame):
        raise TypeError("filter_restaurants must be a pandas DataFrame.")
    if not isinstance(price, str):
        raise TypeError("price must be a string.")

    prices = ['$', '$$', '$$$', '$$$$']
    #filter_price = filter_restaurants[filter_restaurants['price_range'] == price] # pylint: disable=singleton-comparison
    filter_price = filter_restaurants
    filter_price['result'] = filter_price['price_range'].str.contains('|'.join(prices)) # pylint: disable=singleton-comparison
    filter_price = filter_price[filter_price['result'] == True]
    filter_price.drop('result', axis = 1, inplace = True)
    #st.write('price_shortlist: ', filter_price.shape)
    return filter_price
def score_shortlist(filter_price, minimum_rating):
    '''
    Description: Filtering the price-filtered data to only include restaurants
    with a score greater than or equal to the minimum score input by the user
    from '0' to '5'
    ----------
    Execution String: score_shortlist(filter_price, minimum_rating)
    Input:
    filter_price: obtained dishes after filtering for price
    minimum_rating: lowest acceptable score for a restaurant
    Output:
    filtered dataframe of dishes where the restaurant score is higher
    than the specified minimum.
    '''
    # Check for valid input type and value
    if not isinstance(minimum_rating, (float, int)):
        raise TypeError("minimum_rating must be a float or an integer.")
    if minimum_rating < 0 or minimum_rating > 5:
        raise ValueError("minimum_rating must be between 0 and 5 (inclusive).")
    filter_score = filter_price[filter_price['RestaurantScore'] >= minimum_rating]
    #st.write('score_shortlist: ', filter_score.shape)
    return filter_score
def restaurant_category_shortlist(filter_score, restaurant_category_input):
    '''
    Description: Filtering the score-filtered data to only include restaurants
    which match the restaurant category input given by the user.
    ----------
    Execution String: restaurant_category_shortlist(filter_score,"Indian")
    Input:
    filter_score: obtained dishes after filtering restaurant score
    restaurant_category_input: Desired restaurant category from the user
    Output:
    filtered dataframe of dishes where the restaurant category matches the
    user input.
    '''
    if not isinstance(filter_score, pd.DataFrame):
        raise TypeError("filter_score(the first argument) must be a pandas DataFrame.")
    rest_category = df_categories[
        df_categories['Updated Category'].str.contains(
            restaurant_category_input
            )
        ]
    list_rest_category = rest_category.RestaurantCategory.values.tolist()
    #st.write(list_rest_category)
    filter_score['result'] = filter_score['RestaurantCategory'].str.contains(
        '|'.join(list_rest_category)
        )
    filter_rest_category = filter_score[filter_score['result'] == True] # pylint: disable=singleton-comparison
    filter_rest_category.drop('result', axis = 1, inplace = True)
    #st.write(filter_rest_category.shape)
    return filter_rest_category
def food_category_shortlist(filter_rest_category, food_category):
    '''
    Description: Filtering the data obtained after filtering restaurant
    categories. The data is further filtered to accommodate food item categories
    ----------
    Execution String: food_category_shortlist(filter_rest_category,"Other")
    Input:
    filter_rest_category: obtained dishes after filtering restaurant category
    food_category: Desired food item category
    Output:
    filtered dataframe of dishes where the food item category matches the
    user's desired food item category.
    '''
    if not isinstance(filter_rest_category, pd.DataFrame):
        raise TypeError("filter_rest_category(the first argument) must be a pandas DataFrame.")
    if food_category == 'None':
        return filter_rest_category
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
    Execution String: food_category_shortlist(filter_food, "Good")
    Input:
    filter_food: Dishes obtained after filtering the food item categories
    health_inspect_input: Health inspection results option taken from user.
    Output:
    filtered dataframe of dishes where the food item category matches the
    user's health inspection requirement.
    '''
    if not isinstance(filter_food, pd.DataFrame):
        raise TypeError("filter_food(the first argument) must be a pandas DataFrame.")
    acceptable = []
    if health_inspect_input == "Excellent":
        acceptable = ['Excellent']
    elif health_inspect_input == "Good":
        acceptable = ['Excellent', 'Good']
    elif health_inspect_input =='Okay':
        acceptable = ['Excellent', 'Good', 'Okay']
    elif health_inspect_input =='Unrated':
        acceptable = ['Excellent', 'Good', 'Okay', 'Unrated']
    elif health_inspect_input == 'Needs to improve':
        acceptable = ['Excellent', 'Good', 'Okay', 'Unrated', 'Needs to improve']
    else:
        st.error('Invalid Health Inspection result input, try again!', icon="🚨")
        st.stop()
    filter_food['result'] = filter_food['Grade'].str.contains('|'.join(acceptable))
    health_inspection_df = filter_food[filter_food['result'] == True] # pylint: disable=singleton-comparison
    health_inspection_df.drop('result', axis = 1, inplace = True)
    return health_inspection_df

def seating_shortlist(health_inspection_filter, seating_input):
    '''
    Description: Filtering the data based on user's seating preferences.
    ----------
    Execution String: seating_shortlist(health_inspection_df, "13 - 50")
    Input:
    health_inspection_filter: Dishes obtained after filtering for health inspection
    results.
    seating_input: Number of seats option taken from user.
    Output:
    filtered dataframe of dishes where the restaurant has the specified range
    of seats.
    '''
    if not isinstance(health_inspection_filter, pd.DataFrame):
        raise TypeError("health_inspection_filter(the first argument) must be a pandas DataFrame.")

    if seating_input == 'Takeout':
        seating_input = 'No Seating'
    else:
        pass
    acceptable_seating = []
    if seating_input == "No Seating":
        acceptable_seating = ['No Seating']
    elif seating_input == "0 - 12":
        acceptable_seating = ['No Seating', '0 - 12']
    elif seating_input =="13 - 50":
        acceptable_seating = ['No Seating', '0 - 12','13 - 50']
    elif seating_input =="51 - 150":
        acceptable_seating = ['No Seating', '0 - 12','13 - 50', '51 - 150']
    elif seating_input == "151-250":
        acceptable_seating = ['No Seating', '0 - 12','13 - 50', '51 - 150', '151-250']
    elif seating_input == "> 250":
        acceptable_seating = ['No Seating', '0 - 12','13 - 50', '51 - 150', '151-250', '> 250']
    else:
        st.error('Invalid Health Inspection result input, try again!', icon="🚨")
        st.stop()
    seat_filter = health_inspection_filter
    seat_filter['result'] = seat_filter['Seats'].str.contains('|'.join(acceptable_seating))
    seat_filter = seat_filter[seat_filter['result'] == True] # pylint: disable=singleton-comparison
    seat_filter.drop('result', axis = 1, inplace = True)
    return seat_filter
def recommend_food(zip_input, max_dist_input, restaurant_category_input, # pylint: disable=too-many-locals
                   food_category_input, price_input,rating_input, health_inspection_input,
                   seating_input):
    # pylint: disable=too-many-arguments
    '''
    Takes the user responses as input to then filter restaurant and dishes data
    such that the dishes most closely matching user requirements are selected.
    Execution String: recommend_food('98105', 2.5, "Indian","Other", 25.0,2,"Good","13 - 50")
    Input:
    zip_input:
    max_dist_input:
    restaurant_category_input:
    diet_input:
    price_input:
    rating_input:
    health_inspection_input:
    seating_input:
    Output:
    filtered dataframe of top 5 dishes and the restaurants
    '''
    if not isinstance(zip_input,str) or len(zip_input) != 5:
        raise ValueError("Invalid zipcode format. Please enter a 5-digit numeric zipcode.")
    try:
        max_dist_input = float(max_dist_input)
        if max_dist_input <= 0:
            raise ValueError("Maximum distance must be a positive number.")
    except ValueError as exc:
        raise ValueError("Invalid maximum distance. Please enter a valid distance.") from exc

    if not isinstance(price_input, str):
        raise TypeError("price must be a string.")
    if not isinstance(rating_input, (float, int)):
        raise TypeError("rating_input must be a float or an integer.")
    if rating_input < 0 or rating_input > 5:
        raise ValueError("rating_input must be between 0 and 5 (inclusive).")
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
    filter_restaurants = restaurant_category_shortlist(filter_score,
                                                   restaurant_category_input)
    # filter based on dietary preferences
    filter_food_category = food_category_shortlist(filter_restaurants, food_category_input)
    filter_food_category = filter_food_category.sort_values(by = ['RestaurantScore'],
                                          ascending = False)
    health_inspection_filter = health_inspect_shortlist(filter_food_category,
                                                        health_inspection_input)
    seating_filter = seating_shortlist(health_inspection_filter, seating_input)
    df_final = seating_filter.drop_duplicates(subset=['RestaurantName'])
    if df_final.shape[0] >=5: # pylint: disable=no-else-return
        return df_final.head()
    else:
        return seating_filter.head()
def main(): # pylint: disable=too-many-statements, too-many-branches
    # pylint: disable=too-many-locals
    '''
    The web app is rendered through this function.
    User inputs taken through this function.
    '''
    st.markdown(
        "<h1 style='text-align: center; color: white;'>FRAME - Food Recommendations for All Methodical Eaters 🍴</h1>", unsafe_allow_html=True) # pylint: disable=line-too-long
    #st.title("FRAME - Food Recommendations for All Methodical Eaters 🍴")
    placeholder = st.empty()
    with placeholder.form("FRAME_form"):
        st.subheader("Enter your preferences:")
        # Input for user zipcode and max distance
        left_zip, right_dist = st.columns(2)
        zip_input = left_zip.selectbox('Zip code (Seattle only):', options = seattle_zips)
        if zip_input not in seattle_zips:
            st.error('Invalid zipcode, please try again!', icon="🚨")
            st.stop()
        # Input for maximum distance from user
        max_dist_input = right_dist.number_input('Maximum distance preference (miles): ',
                                                 min_value = 0.5,
                                                 max_value = 15.0,
                                                 step = 0.5)
        if isinstance(max_dist_input, float) is False and isinstance(max_dist_input, int) is False:
            st.error('Invalid max distance input, numbers only!', icon="🚨")
            st.stop()
        else:
            pass
        # Input for cuisine and diet restrictions
        left_restaurants, right_food = st.columns(2)
        restaurant_category = ['Other','African', 'American', 'Asian', 'Bakery', 'Breakfast',
                                 'Cafe', 'Chinese', 'Comfort Food', 'Desserts', 'European',
                                 'Healthy', 'Indian', 'Italian', 'Japanese', 'Korean',
                                 'Mediterranean', 'Mexican','Middle Eastern', 'Pizza',
                                 'Seafood', 'Thai', 'Vegan', 'Vegetarian', 'Vietnamese']
        restaurant_category_input = left_restaurants.selectbox('Restaurant Category:',
                                                               options = restaurant_category)
        if restaurant_category_input not in restaurant_category:
            st.error('Invalid restaurant category, try again!', icon="🚨")
            st.stop()
        else:
            pass
        # Input for dietary preferences
        food_item_category = ['Other', 'Appetizers', 'Entrees', 'Beverages',
                              'Sides', 'Salads', 'Platters', 'Desserts', 'Snacks', 'None']
        food_category_input = right_food.selectbox('Food Category',
                                                   options = food_item_category)
        if food_category_input not in food_item_category:
            st.error('Invalid food category, try again!', icon="🚨")
            st.stop()
        else:
            pass
        # Input for price range and rating preference
        left_price, right_rating = st.columns(2)
        price_input = left_price.selectbox('Maximum Price ($): ',
                                           options = ['$', '$$', '$$$', '$$$$'])
        if isinstance(price_input, str) is False:
            st.error('Invalid price input, try again!', icon="🚨")
            st.stop()
        else:
            pass
        # Input for restaurant rating preferences
        rating_input = right_rating.selectbox(
            'Enter restaurant rating preferences (on a scale of 5): ',
            options=['★ & Up', '★★ & Up', '★★★ & Up', '★★★★ & Up', 'None'])
        if rating_input == '★ & Up':
            rating_input = 1
        elif rating_input == '★★ & Up':
            rating_input = 2
        elif rating_input == '★★★ & Up':
            rating_input = 3
        elif rating_input == '★★★★ & Up':
            rating_input = 4
        else:
            rating_input = 0
        if isinstance(rating_input, float) is False and isinstance(rating_input, int) is False:
            st.error('Invalid rating requirement, try again!', icon="🚨")
            st.stop()
        else:
            pass
        # Input for restaurant health inspection
        left_health_inspect, right_seating = st.columns(2)
        health_inspection = ['Excellent', 'Good', 'Okay', 'Unrated', 'Needs to improve']
        health_inspect_input = left_health_inspect.selectbox(
            "Lowest Health Inspection Results you'd settle for: ",
                                            options = health_inspection)
        if health_inspect_input not in health_inspection:
            st.error('Invalid inspection criteria, try again!', icon="🚨")
            st.stop # pylint: disable=pointless-statement
        seating = ['Takeout', '0 - 12','13 - 50', '51 - 150', '151-250', '> 250']
        seating_input = right_seating.selectbox("How extroverted are you feeling today?",
                                     options = seating)
        if seating_input not in seating:
            st.error('Invalid seating criteria, try again!', icon="🚨")
            st.stop # pylint: disable=pointless-statement
        submit = st.form_submit_button("Get FRAMEd!")
    if submit:
        final_filter = recommend_food(zip_input, max_dist_input,
                                      restaurant_category_input, food_category_input,
                                      price_input, rating_input, health_inspect_input,
                                      seating_input)
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
                st.subheader(f'#{i}: {final_filter.iloc[i-1,-4]}')
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
    newmap = fgmap.Fgmap() # pylint: disable=no-member
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
