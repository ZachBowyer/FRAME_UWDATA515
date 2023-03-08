Folium:
Pros: 
    Simple to use
    Probably better fits our project (Can display restaurant on map at a minimum)
Cons:
    Cannot easily remove marker/circles from map object (This means you may have to regenerate map multiple times or edit the html in browser)
    Icon sizes can't be changed (Small feature but there are likely other similar issues)
    Generates html, so forced into web-based solutions for our bigger problem

Google maps api libraries:
Pros: 
    Can give directions, snap to roads, etc. More extensive features. However we may not need these. 
    GMAPS works very well for ipython-based solutions
Cons: 
    Require api key that you need to sign up with a credit card on a free trial
    Complicated
    Does not have a native python library - Third party library must be used
    You have to pay eventually for it