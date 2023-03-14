"""
This python file makes sure everything is properly installed and downloaded
Before you run this file, every needed dependency and python should be installed on 
your local machine.
You can do this with Anaconda. conda env create --name FRAME --file=environment.yml
"""

# Ignoring first because we dont want to set everyone's python PATH or pylintr
# pylint: disable=import-error
from uszipcode import SearchEngine
import gdown

#Automatically download zipcode data to your machine
search = SearchEngine(simple_or_comprehensive=
    SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
zipcode = search.by_zipcode(99338)

# Download data from:
#  https://drive.google.com/drive/folders/1g0Ml_OpA-r1Pre5Td1XlmaNU7H6Wwxm9
# Restaurant Menu
URL1 = 'https://drive.google.com/uc?id=19x38WTsXuYc7hV7CWHJgal9KhuAVyjxP'
gdown.download(URL1, 'data/restaurant-menus.csv', quiet=False)

# Restaurant Data
URL2 = 'https://drive.google.com/uc?id=11jI-5gKmaA_kx3Owv757aqXbSIqkzKWn'
gdown.download(URL2, 'data/restaurants.csv', quiet=False)

# King county inspection data
URL3 = 'https://drive.google.com/uc?id=1EPtMo7mulWnW2sRrZoHHWFfnU54pYmCX'
gdown.download(URL3, 'data/seagov.csv', quiet=False)

# Preprocessed data (Takes too long to run manually)
URL4 = 'https://drive.google.com/uc?id=149o_vBeYkXa0oAGPUNJ3FUeWdFicO-0e'
gdown.download(URL4, 'data/Category_Mapping.csv', quiet=False)

# Preprocessed data (Takes too long to run manually)
URL5 = 'https://drive.google.com/uc?id=10g9vS2VFuGYmxLBCRnxjSvXVLlrpEnKv'
gdown.download(URL5, 'data/Food_and_Restaurant_Data.csv', quiet=False)

#Data for dashboard
URL6 = 'https://drive.google.com/uc?id=1Av8qtRWFgKEl74Y0GzV8GiMOIjKDeI5s'
gdown.download(URL5, 'data/Datafordashboard.csv', quiet=False)
