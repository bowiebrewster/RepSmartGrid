import matplotlib.pyplot as plt
import copy
import random

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
        self.costs = 25000
        self.path = f'data/district_{number}/district-{number}_'
        self.colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']
        self.batteries = []
        self.houses = []
        self.load_files()
        self.connections = {battery_obj: None for battery_obj in self.batteries}

    def load_files(self):
        files = [self.path + 'batteries.csv', self.path + 'houses.csv']
        for filename in files:
            with open(filename, 'r') as file:
                data = file.readlines()[1:]
                for i, row in enumerate(data):
                    row = row.replace('"', '').split(',')
                    x, y, OC = int(row[0]), int(row[1]), float(row[2].rstrip())
                    if len(data) < 10:
                        self.batteries.append(Battery(i + 1, x, y, OC))
                    else:
                        self.houses.append(House(i + 1, x, y, OC))

    def random_allocation(self, show=True):
        j = 0
        while not self.is_feasible():
            if j % 100 == 0:
                print(j)

            houses = copy.deepcopy(self.houses)
            random.shuffle(self.houses)
            for i, battery in enumerate(self.connections.keys()):
                self.connections[battery] = houses[i * 30: (i + 1) * 30]
            j += 1
        print("Feasible allocation found!")
        if show:
            self.show_connections(title = 'random')

    def greedy_allocation(self, show=True):
        for battery in self.connections.keys():
            total_output = 0
            print(self.nearest_neighbors(xbattery=battery.x, ybattery=battery.y))
            while total_output <= battery.capacity:
                pass
                # for house in self.nearest_neighbors(xbattery=battery.x, ybattery=battery.y).keys():
                #     if total_output + house.output < battery.capacity:
                #         total_output += house.output
                #         self.connections[battery] = house
        
        # if show:
        #     self.show_connections(title = 'greedy')

    def nearest_neighbors(self, xbattery, ybattery):
        # finds houses that are closest by the given coordinates
        house_locations = {house.number: (house.x, house.y) for house in self.houses}
        

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
        plt.grid(which='major', color='#57838D', linestyle='-')
        plt.minorticks_on()
        plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
        plt.savefig(f'figures/{title}/{title.capitalize()} allocation: €{self.costs}')

    def calculate_costs(self):
        total_distance = 0
        for battery, houses in self.connections.items():
            for house in houses:
                total_distance += abs(battery.x - house.x) + abs(battery.y - house.y)
        self.costs += 9 * total_distance

if __name__ == "__main__":
    district1 = District(1)
    district1.greedy_allocation(show=True)