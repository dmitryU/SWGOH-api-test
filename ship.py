class Ship:
    def __init__(self, name, power, description):
        self.name = name
        self.power = power
        self.description = description
    def serialize(self):
        print ("Name: " + self.name)
        print ("Power: " + str(self.power))
        print ("Description: " + self.description)
