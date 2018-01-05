#!/usr/bin/env python3
import requests
import json
import pickle
from character import *

response = requests.get('https://swgoh.gg/api/characters')
json_data = response.json()
characters = []

for idx, c in enumerate(json_data):
    newChar = Character(c['name'], c['power'], c['description'])
    characters.append(newChar)

with open('charData.pkl', 'wb+') as file:
    pickle.dump(characters, file)
