import matplotlib.pyplot as plt

class House():
    def _init_(self, x, y, output):
        self.x = x
        self.y = y
        self.output = output

class Battery():
    def _init_(self, x, y, capacity):
        self.x = x
        self.y = y
        self.capacity = capacity

class District():
    def _init_(self):
        self.batteries = []
        self.houses = []
        self.load() # laad alle huizen en batterijen in en sla op in self.batteries en self.houses
        connections = {battery_obj: None for battery_obj in self.batteries}

    def load(self):
        files = [] # de twee bestanden opslaan in lijst
        for filename in files:
            pass # open en lees regel per regel de bestanden
            # per regel check welke elementen de coordinaten zijn en welke de output/capacity
            # als de lengte van een bestand klein is dan is dat het bestand van de batterijen
                # maak per x, y en capacity van elke regel een battery object aan en geef deze waarden mee
                # append dit batterij object aan de lijst self.batteries
            # andere bestand is vd huizen
                # maak per x, y en output van elke regel een house object aan en geef deze waarden mee
                # append dit huis object aan de lijst self.houses 
    
    def allocate(self):
        # vul de dictionary self.connections in
        # de keys zijn al ingevuld, dat zijn alle batterij objecten
        # de values zijn de huizen die aan een batterij gekoppeld zijn
        # hoe kiezen we welke huizen we gebruiken?
        pass

    def connect(self):
        for battery, houses in self.connections.items():
            for house in houses:
                xsteps = [battery.x, house.x, house.x]
                ysteps = [battery.y, battery.y, house.y]
                plt.plot(xsteps, ysteps)
        plt.show()

    def visualise(self):
        pass
        # laat plot zien? of is dat al voldoende bij connect
        # we moeten ook eigenlijk de huizen en de batterijen zelf als scatter laten zien
        # for battery in self.batteries:
            # plt.scatter is iets geloof ik dat je de x en y coordinaten meegeeft
        # for house in self.houses:
            # plt.scatter
        # in welke volgorde visualiseren? denk eerst handig als we een scatter van huizen en batterijen zien

    def costs(self):
        pass
        # bereken kosten van de lengte van elke connectie tussen huis en batterij
        # self.fixedcosts = 5000 * len(self.batteries)
        # for battery, houses in self.connections.items():
            # for house in houses:
                # manhattan_distance = abs(battery.x - house.x) + abs(battery.y - house.y)
                # self.varcosts += 9 * manhattan_distance
        # return self.fixedcosts + self.varcosts