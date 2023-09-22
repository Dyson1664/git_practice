# 2020-21/en.1.clubs.json
import requests
from dotenv import load_dotenv
import os
import json



url = 'https://raw.githubusercontent.com/openfootball/football.json/master/2015-16/en.1.clubs.json'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # This automatically converts the JSON into a Python dictionary
    clubs = data['clubs']
    for club in clubs:
        print(club['name'])
else:
    print(f"Failed to retrieve data: {response.content}")


