#!/usr/bin/env python3

import json
import pickle
from objects import *

json_data = ''
guild_units = []
with open('units.json', 'r') as file:
    json_data = json.load(file)

units = []

for name, instances in json_data.items():
    new_unit_dict = {name:instances}
    unit_instances = []

    for i in instances:
        keys = i.keys()
        unit_type = ''
        for idx in keys:
            if idx == 'gear_level':
                unit_type = 'character'
                break
            else:
                unit_type = 'ship'
        if unit_type == 'character':
            new_instance = GuildInstance(i['gear_level'], i['power'], i['level'], i['url'], i['combat_type'], i['rarity'], i['player'])
            unit_instances.append(new_instance)

    new_unit = GuildUnit(name, unit_instances)
    units.append(new_unit)

ro2 = Guild("Rule of Two Reloaded")
ro2.setUnits = units
with open("ro2.pkl", "wb+") as file:
    pickle.dump(ro2, file)
