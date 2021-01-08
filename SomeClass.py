import matplotlib.pyplot as plt
import copy
import random
import numpy as np

class House():
    def __init__(self, number, x, y, output):
        self.number = number
        self.x = x
        self.y = y
        self.output = output

    def __str__(self):
        return self.number

class Battery():
    def __init__(self, number, x, y, capacity):
        self.number = number
        self.x = x
        self.y = y
        self.capacity = capacity

    def __str__(self):
        return self.number

class District():
    def __init__(self, number):
        self.number = number
        self.path = f'data/district_{number}/district-{number}_'
        self.batteries = []
        self.houses = []
        self.load_files() # laad alle huizen en batterijen in en sla op in self.batteries en self.houses
        self.costs = 25000
        self.connections = {battery_obj: None for battery_obj in self.batteries}

    def load_files(self):
        files = [self.path + 'batteries.csv', self.path + 'houses.csv'] # de twee bestanden opslaan in lijst
        for filename in files:
            with open(filename, 'r') as file:
                data = file.readlines()[1:]
                # per regel check welke elementen de coordinaten zijn en welke de output/capacity
                for i, row in enumerate(data):
                    row = row.replace('"', '').split(',')
                    x, y, OC = int(row[0]), int(row[1]), float(row[2].rstrip())
                    # als de lengte van een bestand klein is dan is dat het bestand van de batterijen
                    if len(data) < 10:
                        # maak per x, y en capacity van elke regel een battery object aan en geef deze waarden mee
                        self.batteries.append(Battery(i + 1, x, y, OC))
                    # andere bestand is vd huizen
                    else:
                        # maak per x, y en output van elke regel een house object aan en geef deze waarden mee
                        self.houses.append(House(i + 1, x, y, OC))

    def random_allocation(self):
        # vul de dictionary self.connections randomly in
        houses = copy.deepcopy(self.houses)
        random.shuffle(houses)
        for i, battery in enumerate(self.connections.keys()):
            self.connections[battery] = houses[i * 30: (i + 1) * 30]

    def show_grid(self):
        for house in self.houses:
            plt.scatter(house.x, house.y, c='#004C46', marker='*')
        for battery in self.batteries:
            plt.scatter(battery.x, battery.y, c='#004C46', marker='s')
        self.connect_gridlines()
        plt.grid(b=True, which='major', color='#57838D', linestyle='-')
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#57838D', linestyle='-', alpha=0.2)
        plt.show()
    
    def connect_gridlines(self):
        for battery, houses in self.connections.items():
            for house in houses:
                xsteps = [battery.x, house.x, house.x]
                ysteps = [battery.y, battery.y, house.y]
                plt.plot(xsteps, ysteps)

    def calculate_costs(self):
        # bereken kosten van de lengte van elke connectie tussen huis en batterij
        for battery, houses in self.connections.items():
            for house in houses:
                manhattan_distance = abs(battery.x - house.x) + abs(battery.y - house.y)
                self.costs += 9 * manhattan_distance
        return self.costs

if __name__ == "__main__":
    district1 = District(1)
    district1.random_allocation()
    district1.show_grid()
    district1.connect_gridlines()