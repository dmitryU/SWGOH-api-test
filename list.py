#!/usr/bin/env python3
import pickle
characters = []
with open('charData.pkl', 'rb') as file:
    characters = pickle.load(file)
for c in characters:
    c.serialize() 
    print()

