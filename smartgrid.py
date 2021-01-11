import matplotlib.pyplot as plt
import copy
import random
import itertools

class House():
    def __init__(self, number, x, y, output):
        self.number = number
        self.x = x
        self.y = y
        self.output = output
        self.is_available = True

    def __str__(self):
        return self.number

class Battery():
    def __init__(self, number, x, y, capacity):
        self.number = number
        self.x = x
        self.y = y
        self.capacity = capacity
        self.is_full = False

    def is_feasible(self, house):
        '''Return True if battery can take given house and subtract 
        house output from battery capacity.'''
        if self.capacity - house.output < 0:
            return False
        self.capacity -= house.output
        return True

    def __str__(self):
        return self.number

class District():
    def __init__(self, number):
        self.number = number
        self.reset_costs()
        self.path = f'data/district_{number}/district-{number}_'
        self.colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']
        self.batteries = []
        self.houses = []
        self.load_files()
        self.connections = {battery_obj: [] for battery_obj in self.batteries}
        self.all_distances = {battery: {house: self.get_mhd(battery, house) for house in self.houses} for battery in self.batteries}

    def load_files(self):
        files = [self.path + 'batteries.csv', self.path + 'houses.csv']
        for filename in files:
            with open(filename, 'r') as file:
                data = file.readlines()[1:]
                for i, row in enumerate(data):
                    row = row.replace('"', '').split(',')
                    x, y, OC = int(row[0]), int(row[1]), float(row[2].rstrip())
                    if len(data) == 5:
                        self.batteries.append(Battery(i + 1, x, y, OC))
                    else:
                        self.houses.append(House(i + 1, x, y, OC))

    def random_allocation(self, show=True):
        j = 0
        # shuffle de set van huizen totdat je wel een feasible oplossing hebt
        while not self.is_feasible():
            if j % 100 == 0:
                # iteraties bijhouden
                print(j)

            houses = copy.deepcopy(self.houses)
            random.shuffle(self.houses)
            # pak voor elke batterij 30 huizen
            for i, battery in enumerate(self.connections.keys()):
                self.connections[battery] = houses[i * 30: (i + 1) * 30]
            j += 1

        print("Feasible allocation found!")
        if show:
            self.show_connections(title = 'random')

    def greedy_allocation(self, show=True):
        # op hoeveel manieren kan je 5 batterijen sorteren?
        # dit maakt een set van de batterijen op bepaalde volgordes waar je doorheen kan itereren
        orderings = list(itertools.permutations(self.batteries, 5))
        for i, battery_ordering in enumerate(orderings):
            # voor elke batterij in de order
            for battery in battery_ordering:
                # dict met key huis object en value manhattan distance als het huis nog gekozen kan worden
                distances = {house: mhd for house, mhd in self.all_distances[battery].items() if house.is_available}
                # als de batterij nog niet vol is en distances nog niet leeg is
                while not battery.is_full and distances:
                    # zoek de minimale distance en pak het bijbehorende huis
                    house_to_add = min(distances, key=distances.get)
                    # kijk of je dit huis kan toevoegen aan de batterij
                    if battery.is_feasible(house_to_add):
                        # voeg huis toe aan de connections bij deze batterij
                        self.connections[battery].append(house_to_add)
                        # verwijder dit huis vervolgens uit de dictionary van alle distances (want je wil dit huis niet meer kunnen kiezen)
                        mhd = distances.pop(house_to_add)
                        house_to_add.is_available = False
                    else:
                        # als dit huis niet toegevoegd kan worden dan is de batterij dus vol
                        battery.is_full = True

            # dan is dus elk huis (alle 150) gealloceerd aan een batterij 
            if sum([len(x) for x in self.connections.values()]) == 150: 
                print("Feasible allocation found!")
                if show:
                    # laat grafiek zien in mapje
                    self.show_connections(title='greedy')
            
            # reset alle huizen, batterijen, connecties en kosten
            # zodat je met de volgende iteratie met een schone lei begint
            self.reset_house_availability()
            self.reset_battery_capacity()
            self.reset_connections()
            self.reset_costs()
    
    def swap(self):
        # get 2 distinct random batteries
            # get random house from each 
            # make swap
        pass

    def reset_house_availability(self):
        for house in self.houses:
            house.is_available = True
    
    def reset_battery_capacity(self):
        for battery in self.batteries:
            battery.capacity = round(battery.capacity + sum([house.output for house in self.connections[battery]]), 1)
            battery.is_full = False    
    
    def reset_connections(self):
        self.connections = {battery_obj: [] for battery_obj in self.batteries}
    
    def get_mhd(self, battery, house):
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def is_feasible(self):
        for battery, houses in self.connections.items():
            if not houses:
                return False
            total_output = sum([house.output for house in houses])
            if total_output > battery.capacity:
                return False
        return True
    
    def show_connections(self, title):
        for battery, houses in self.connections.items():
            plt.scatter(battery.x, battery.y, c=self.colors[battery.number - 1], marker='s')
            for house in houses:
                plt.scatter(house.x, house.y, c=self.colors[battery.number - 1], marker='*')
                xsteps = [battery.x, house.x, house.x]
                ysteps = [battery.y, battery.y, house.y]
                plt.plot(xsteps, ysteps, c=self.colors[battery.number - 1])
        self.calculate_costs()
        print(self.costs)
        plt.grid(which='major', color='#57838D', linestyle='-')
        plt.minorticks_on()
        plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
        plt.savefig(f'figures/{title}/{title.capitalize()} allocation: €{self.costs}')

    def calculate_costs(self):
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)
    
    def reset_costs(self):
        self.costs = 25000

if __name__ == "__main__":
    district1 = District(2)
    district1.greedy_allocation(show=True)