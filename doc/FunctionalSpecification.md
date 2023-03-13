# Background:
This project attempts to recommend users specific dishes based on their needs rather than restaurants.  
The solution to this specific problem is to use a filter based approach through a web-hosted application.   
A more extensive description can be found in README.md. 

# User profiles
##  Story #1 - 
#### Who: General user (this can be anybody)  
#### Need: Browsing for a meal, looking for suggestions  
#### Interaction method: Through our web application  
#### Needs: 5 Recommendations based on inputs (needs)  
#### Skills: Basic website navigation, simple UI required  
--
## Story #2 - 
#### Who: Restaurant owners  
#### Want: Menus/restaurants posted, wants them recommended to as many people as possible  
#### Interaction methods: Through our web application   
#### Needs: Want to search up information about their restaurant/menus/etc as see how often they are being  recommended
#### Skills: Basic website navigation, knowledge of ingredients/calories/menus  
--
## Story #3 - 
#### Who: Developers
#### Want: Debug mode/Console
#### Interaction methods: Through a command line
#### Needs: Ability to debug code and see hidden variables/outputs
#### Skills: Console navigation, python k

# Data sources:
Uber Eats Restaurants and Menus - https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus    
   
This dataset contains two files:   
Restaurants.csv (40228 rows, 11 columns)    
* id (int64): 1-40228      
* position (int64): Irrelevant    
* Name (String): unspecified format    
* score (float64): 1.3-5.0, 45.21% null values  
* ratings (float64): 10-500, 44.6% null values  
* category (String): unspecified format, 0.05% null values  
* price-range: Either $, $$, $$$, or $$$$ (Inexpensive, Moderately expensive, Expensive, Very   Expensive), 16.5% null values  
               https://stackoverflow.com/questions/40005100/what-is-the-pricerange-parameter-for-google-structured-data-reviews/40112652#40112652    
               (Seems arbitrary)    
* full_address (string): Unspecified format, 0.69% null values  
* zip_code (string): Unspecified format, 0.71% null values  
* lat (float64): 0 - 48.964  
* lng (float64): -123.841 - 0  
  
restaurant-menus.csv (3375211 rows, 5 columns)
* restaurant-id: (int64) - 1-40228
* category (String): Unspecified format
* name (String): Unspecified format
* description (String): Unspecified format, 26.9% null values
* price: (String, float followed with ' USD', EX: '5:99 USD')  
From this data, we have 1740 Seattle-based restaurants, that combine for 99643 menu items.  

--  

Googlemaps api in conjunction with the googlemaps python package. Documentation can be found here https://developers.google.com/maps/documentation (Pulls from database for address information and trips)

--     
Potential: Uber eats scraper - https://github.com/gsunit/Extreme-Uber-Eats-Scraping   

# Use cases:
Explicit: User wants to know what to eat for dinner/breakfast/lunch
  * Navigate to website url
  * Select filters
    * Distance
    * Allergies
    * Etc...
  * Click search button
  * If desired result comes up: User can click on it
    * Show website url if it exists
    * If website url does not exist, link to show location of restaurant on google maps
  * If desired result does not come up, allow user to re-filter 

Explicit: User wants to search up a specific restaurant and view it's menu
  * Navigate to website url
  * Use a search bar to find a specific restaurant
     * User is given a link to the restaurant
       * Show google maps if link does not exist
     * All menu items shown

Explicit: User wants to filter all menu items from a specific restaurant
  * Navigate to website url
  * Use a search bar to find a specific restaurant
  * User clicks on desired result
  * From there, filters will show up
    * Select filters
  * Click Search Button
    * If desired result comes up: User can click on it
    * Show website url if it exists
    * If website url does not exist, link to show location of restaurant on google maps
  * If desired result does not come up, allow user to re-filter 

Implicit: User wants a place on the internet to get multiple food recommendations based on filters that are not available with existing platforms
* Our url exists, and people can navigate to it
