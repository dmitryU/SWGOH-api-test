class Character:
    def __init__(self, baseId, name, power, description, url, image):
        self.baseId = baseId
        self.name = name
        self.power = power
        self.description = description
        self.url = url
        self.image = image
    def serialize(self):
        print ("Name: " + self.name)
        print ("Power: " + str(self.power))
        print ("Description: " + self.description)

class Ship:
    def __init__(self, baseId, name, power, description, url, image):
        self.baseId = baseId
        self.name = name
        self.power = power
        self.description = description
        self.url = url
        self.image = image
    def serialize(self):
        print ("Name: " + self.name)
        print ("Power: " + str(self.power))
        print ("Description: " + self.description)

class GuildInstance:
    def __init__(self, gear_level, power, level, url, combat_type, rarity, player):
        self.gear_level = gear_level
        self.power = power
        self.level = level
        self.url = url
        self.combat_type = combat_type
        self.rarity = rarity
        self.player = player
    def serialize(self):
        print ("Player: " + self.player)
        print ("\tGear Level: " + str(self.gear_level))
        print ("\tPower: " + str(self.power))
        print ("\tLevel: " + str(self.level))
        print ("\tRarity: " + str(self.rarity))
    def __str__(self):
        return "%s;%d;%d;%d;%d" % (self.player, self.gear_level, self.power, self.level, self.rarity)

class GuildUnit:
    def __init__(self, name, GuildInstances):
        self.name = name
        self.instances = GuildInstances
    def serialize(self):
        print ("Name: " + self.name)
        for i in self.instances:
            i.serialize()

class Guild:
    def __init__(self, name):
        self.name = name
    def setUnits(self, units):
        self.units = units