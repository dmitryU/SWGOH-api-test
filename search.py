#!/usr/bin/env python3
import pickle
characters = []
with open('charData.pkl', 'rb') as file:
    characters = pickle.load(file)
usrIn = input ("Enter character name: ")
print ()

for c in characters:
    if usrIn.lower() in c.name.lower():
        c.serialize() 
        print()

