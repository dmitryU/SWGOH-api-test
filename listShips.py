#!/usr/bin/env python3
import pickle
ships = []
with open('shipData.pkl', 'rb') as file:
    ships = pickle.load(file)
for s in ships:
    s.serialize() 
    print()

