#!/usr/bin/env python3
import pickle
with open('guild.pkl', 'rb') as file:
    guild = pickle.load(file)

name = input ("Enter character name to search: ")


with open('charstats.csv', 'w') as file:
    for unit in guild.setUnits:
        if unit.name == name:
            file.write('Player;Gear level;Power;Level;Rarity\n')
            for instance in unit.instances:
                s = str(instance)
                print(s)
                file.write(s + '\n')
            break
