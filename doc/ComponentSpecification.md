# Software components
Web-hosted application
- Reasoning: We ultimately want our tool to be publically available through a website url. 
- What it does: Connects to the internet and provides an interface for our filters/algorithms/visualizations.  
- Inputs required: Requires a connection to the internet and port forwarding.  
- Provided outputs: GUI to view visualizations, provide input, and manipulate filters.  

Dynamic map creating module
- Reasoning: We would like to show the user their location relative to the restaurant they want to order from. We would also like to show directions to that restaurant if possible.   
- What it does: Creates dynamic maps based on the user's locations, provides pins for the location of the user and the restaurant, and draws polylines to represent directions from the user's location to the restaurant.  
- Inputs required: Coordinates of user (Lat, Lon), Coordinates of target restaurant
- Provided outputs: Json of directions, which are used to create a map that has pins and directions.  

Filtering module:
- Reasoning: We need to have a mechanism that can recommend dishes to users.  
- What it does: Filters out choices the user may not enjoy based on their preferences.  
- Inputs required: User's preferences for foods, IE: Allergies, minimum distance, food type, etc.  
- Provided outputs: A list of the top 10 dishes/restaurants based on the user's choices  

# Interactions to accomplish use-cases
# Use cases:
## Case: User wants to know what to eat for dinner/breakfast/lunch
For this use case, we first need our user to navigate to our url, which can only be possible if our web-hosted application is up and running. 
Next, in order to choose a food, they must input their information and filters, which is also depending on the web application working. 
After that, the filtering module will determine what foods best fit the user's needs.
When the user decides on a food, then the location and direction to that restaurant will be provided bu the dynamic map creating module.    
![alt text](../images/UseCaseInteractionGraph1.png)

## Case: User wants to search up a specific restaurant and view it's menu  
Again, the user must navigate to our url, which can only be possible if the web application is running.  
Next, the user must input a restaurant name in a search bar. 
From there, our filtering module will return the restaurant menu data if it exists, else it will do nothing.  
Then, if the user selects the restaurant all menu data will be shown.  
If the user wants a specific item from that menu, they can select it, which will result in map information being generated (See use case above).  
## Case: User wants to filter all menu items from a specific restaurant  
The user must navigate to our url, which can only be possible if the web application is running. 
From there, our filtering module will return the restaurant menu data if it exists, else it will do nothing.  
Then, if the user selects the restaurant all menu data will be shown.  
Next, in order to choose a food, they must input filters. 
When the user decides on a food, then the location and direction to that restaurant will be provided bu the dynamic map creating module.  

## Case: User wants a place on the internet to get multiple food recommendations based on filters that are not available with existing platforms  
This is an implicit use case, and is already described from the three use-cases above.  

# Preliminary plan
Week 1:
- Ideate the tool
- Identify, Collect and clean data from relevant sources.
- Explore and analyze the data to identify any patterns or trends.
- Develop and test the filtering system to narrow down food choices based on user preferences.
- Success of Week 1: Have the data in hand and define all expectations

Week 2:
- Implement the recommendation algorithm to suggest 5 food items based on the user's selections.
- Create a prototype of the web-accessible application using Streamlit.
- Develop and test the functionality for displaying restaurant links and maps.
- Success of Week 2: Successful recommendation algorithm and a wireframe of the frontend

Week 3:
- Refine and optimize the recommendation algorithm for better accuracy and performance.
- Improve the user interface and add visualizations to make the app more appealing and user-friendly.
- Test the application with a small group of beta users to get feedback and make necessary adjustments.
- Success of Week 3: Improvised frontend, smooth running application without any bugs

Week 4:
- Finalize the application and deploy it to a web server for public use.
- Conduct final testing and debugging to ensure the app is running smoothly and efficiently.
- Prepare a report and a demo video to showcase the project and its features.
- Success of Week 4: Completion of end to end project