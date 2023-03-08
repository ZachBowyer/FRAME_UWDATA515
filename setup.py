"""
This python file makes sure everything is properly installed and downloaded
Before you run this file, every needed dependency and python should be installed on your local machine
You can do this with Anaconda. conda env create --name FRAME --file=environment.yml
"""
from uszipcode import SearchEngine
import gdown

#Automatically download zipcode data to your machine
search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
zipcode = search.by_zipcode(99338)

#Run all unit tests, if they all pass/run then the software has to be correctly installed (WIP)
# Download data from:
#  https://drive.google.com/drive/folders/1g0Ml_OpA-r1Pre5Td1XlmaNU7H6Wwxm9
# Restaurant Menu
url1 = 'https://drive.google.com/uc?id=19x38WTsXuYc7hV7CWHJgal9KhuAVyjxP'
output = 'data/restaurant-menus.csv'
gdown.download(url1, output, quiet=False)

# Retaurant Data
url2 = 'https://drive.google.com/uc?id=11jI-5gKmaA_kx3Owv757aqXbSIqkzKWn'
output = 'data/restaurants.csv'
gdown.download(url2, output, quiet=False)

# King county inspection data
url3 = 'https://drive.google.com/uc?id=1EPtMo7mulWnW2sRrZoHHWFfnU54pYmCX'
output = 'data/seagov.csv'
gdown.download(url3, output, quiet=False)

