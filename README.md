# FRAME - Food Recommendations For all Methodical Eaters
University of Washington - DATA515  
Final Project  
2/12/2023  
Arjun Sharma  
Zachary Bowyer  
Adithyaa Vassen  
Raman SV  

# Project description:
This project aims at improving on what current food delivery apps do, which is recommendation.  
Specifically, instead of suggesting restaurants, the tool would suggest what meals/orders one should    
buy based on various filters. These filter would consist of things like: Location, Cuisine type, Food  
Type, Calories Per Serving, Max Distance, Allergies, Price Range, Restaurant Rating, etc.  

# Project type
This project is of the predefined class type: 'Tool'. We consider it a tool because it is simply a  
improvement/modification on existing solutions to the food recommender problem.  

# Questions of interest
1. Is simple filtering enough? Or it is necessary to use a more complicated recommender system?  
2. Are there any apis we can use for data like uber?  
3. Are the formats of menus easily readable, or do we need to scrape text from images?  
4. Will we be crossreferencing datasets/apis? If so, how would we avoid duplicates? For example: 
   'McDonalds' vs 'MCDONALDS' vs 'McDonald's' vs 'McDonalds Restaurant', etc.  
5. How will we address the issue of no data being available based on current filters?  
6. How complicated will it be to fuse/merge our datasets?  

# Goal for the project output (What is going to be produced?)  
Top 10 dishes that align with user's preferences/filters. Extra details about dish and restaurant given to users if they click on specific recommendation.   

# Data sources:
1. Uber Eats Restaurants and Menus - https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus  
2. New York Public Library (What's on the menu?) - https://menus.nypl.org/data  
3. Data.gov - https://catalog.data.gov/dataset?tags=restaurant    
4. Yelp Review - https://www.yelp.com/dataset  

# Proposal slide: 
![alt text](images/ProposalSlide.png)