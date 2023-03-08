## Dummy Streamlit App

The app takes user inputs and performs filtration of the data to recommend the top 5 closest dishes.
The logic is based on the dummy data available at this time.

# Brief overview of the logic:
1. Takes user input which includes the following:
  - User's name
  - Zipcode (Location input method will be updated)
  - Maximum acceptable distance
  - Cuisine Preference
  - Dietary Preference
  - Max Price
  - Minimum Restaurant Score

2. Filters the data in the following steps:
  i. Restaurants within acceptable distance.
  ii. From (i), retain all the dishes that cost below the Max Price.
  iii. From (ii), retain all the dishes where the restaurant has a higher rating than the Minimum Restaurant Score.
  iv. From (iii), retain only those dishes where the dish belongs to the selected cuisine.
  v. from (iv), retain only those dishes where the dish falls under the specified dietary preferences.
  
3. Displays the top 5 dishes with the following information: 
  - Dish name, 
  - price, 
  - description, 
  - restaurant name, and
  - restaurant address 
in decreasing order of 'Score'.

5. Displays the map with 5 points, each representing the restaurant location.
Note: Currently, the app displays random points on the map, this will be updated after integration with google maps. 
