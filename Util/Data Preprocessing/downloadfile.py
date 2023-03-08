# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 19:48:17 2023

@author: adithyaa
"""

import gdown

# Restaurant Menu
url1 = 'https://drive.google.com/uc?id=19x38WTsXuYc7hV7CWHJgal9KhuAVyjxP'
output = 'restaurant-menus.csv'
gdown.download(url1, output, quiet=False)

# Retaurant Data
url2 = 'https://drive.google.com/uc?id=11jI-5gKmaA_kx3Owv757aqXbSIqkzKWn'
output = 'restaurants.csv'
gdown.download(url2, output, quiet=False)

# King county inspection data
url3 = 'https://drive.google.com/uc?id=1EPtMo7mulWnW2sRrZoHHWFfnU54pYmCX'
output = 'seagov.csv'
gdown.download(url3, output, quiet=False)

