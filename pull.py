#!/usr/bin/env python3
import requests
import json
import pickle
from objects import *

response = requests.get('https://swgoh.gg/api/characters')
json_data = response.json()
characters = []

for idx, c in enumerate(json_data):
    newChar = Character(c['base_id'], c['name'], c['power'], c['description'], c['url'], c['image'])
    characters.append(newChar)

response = requests.get('https://swgoh.gg/api/ships')
json_data = response.json()
ships = []

for s in json_data:
    newShip = Ship(s['base_id'], s['name'], s['power'], s['description'], s['url'], s['image'])
    ships.append(newShip)

response = requests.get('https://swgoh.gg/api/guilds/34508/units')
json_data = response.json()
with open('units.json','w+') as file:
    json.dump(json_data, file)

with open('charData.pkl', 'wb+') as file:
    pickle.dump(characters, file)

with open('shipData.pkl', 'wb+') as file:
    pickle.dump(ships, file)
