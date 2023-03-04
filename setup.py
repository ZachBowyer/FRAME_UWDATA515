"""
This python file makes sure everything is properly installed and downloaded
Before you run this file, every needed dependency and python should be installed on your local machine
You can do this with Anaconda. conda env create --name FRAME --file=environment.yml
"""
from uszipcode import SearchEngine

#Automatically download zipcode data to your machine
search = SearchEngine(simple_or_comprehensive=SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive)
zipcode = search.by_zipcode(99338)

#Run all unit tests, if they all pass/run then the software has to be correctly installed (WIP)
