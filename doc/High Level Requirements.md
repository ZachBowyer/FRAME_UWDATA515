# The main requirements for this website will be - (WE MUST IMPLEMENT THESE AT A MINIMUM)
  1) User uses filters that align with their needs in terms of food items that they are looking for.
  2) The result displays 5 food items based on the selection - these 5 items need not be from the same restaurant. 
  3) The result displays 3 links - the restaurant website(if available), further (all) menu items from the restaurant, and the google maps directions.  (DO NOT EMBED INTO WEBAPP)
       (How about 2 links, replacing one with the embedded google maps, where pin has url as tooltip)
  4) We need a web-accessible application for the users to interface with 
     (Options: Tableau, Streamlit, PowerBI, Flask/Django)
     
     Link to the web app: https://arjun-sc31-data-515-demonstration-app-hj40h8.streamlit.app/
  5) We need a debug/development mode/console for the live website

# Features to consider - (Extra stuff if we have time)
  1) User tracking and storing data of inputs and outputs (May be time-consuming as in a backend)
  2) Further 5 results if the first 5 weren't appetizing enough
  3) Search by restaurant and rank their hits and then have filter options
  4) If we are storing data, we can develop a recommender system based on user profile and inputs (Requires 1)
  5) Track hits of restaurants/menus (Naive counter, can get abused by bots/vpn)
  6) Create multiple views - customer, restaurant owner, website developers/debuggers
      (Does not require 1, button for changing views)
  7) Cross platform to mobile (Dependent on web tools we use)
  8) Keep track of website hits (Bottable)
  9) Keep logs for debugging (requires backend)
  10) Have popular-based filters (require backend)
  11) Have rating based filter 
  11) Embed text-reviews on website



# ROLES/TASK:
# Arjun: 
  * Website design
  * Website hosting research
  * Documentation
# Zach: 
  * Explore data/APIS
  * Documentation
  * Enforce pylint (PEP8) format for all python files
  * Git repo manager (All pull request except for own, own goes to someone else)
# Raman: 
  * Initial hosting
  * Research hosting options
  * Finalizing all documentation
# Adi: 
  * Project Manager
  * Explore data/APIS
  * Documentation

# Unassigned ideas:
Backend (If needed)
Testing (Modular, integration)
