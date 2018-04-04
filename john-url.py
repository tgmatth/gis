'''**********************************************
* Assignment 3C Python Programming              *
* John Goodman Jr                               *
* ISYS 5103 Data Analytic Fundamentals          *
* Python version 3.6.3                          *
**********************************************'''
# Import statements for program
import urllib
import requests
from pprint import pprint

# set the main url for the api with the api key
main_api = 'http://www.omdbapi.com/?apikey=7dec2e57&'


# get the user's input for the movie or tv show and store it in variable 'title'
title = input('Tell me your favorite Movie or TV Show' '\n')

# establish variable 'url' concatenating main_api and api parameters for searching the database
url = main_api + urllib.parse.urlencode({'s': title})

# using requests module, call and get back data based on user input (title)
json_data = requests.get(url).json()

# print title to user and successful message
print(title + ' is a great show!  Here is the results:\n')

# pretty print the json data that was returned
pprint(json_data)