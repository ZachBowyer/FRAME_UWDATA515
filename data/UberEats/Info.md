In the future if we want: https://github.com/Kaggle/kaggle-api

For now, head over to https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus?resource=download 
and unzip the files to this directory

Reminder .csv files are in gitignore. 

pylint command: python -m pylint profile_uber_eats.py

# Uber Eats Restaurants and Menus - https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus    
This dataset contains two files:   
Restaurants.csv (40228 rows, 11 columns)    
* id (int64): 1-40228      
* position (int64): Irrelevant    
* Name (String): unspecified format    
* score (float64): 1.3-5.0, 45.21% null values  
* ratings (float64): 10-500, 44.6% null values  
* category (String): unspecified format, 0.05% null values  
* price-range: Either $, $$, $$$, or $$$$ (Inexpensive, Moderately expensive, Expensive, Very Expensive), 16.5% null values  
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