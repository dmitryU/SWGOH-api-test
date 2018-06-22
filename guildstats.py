#!/usr/bin/env python3
import pickle
with open('guild.pkl', 'rb') as file:
    guild = pickle.load(file)

for unit in guild.setUnits:
    players = []
    for instance in unit.instances:
        players.append(instance.player)        
    print("%s;%d;%s" % (unit.name, len(unit.instances), players))
