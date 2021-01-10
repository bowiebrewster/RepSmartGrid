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
        self.costs = 25000
        self.path = f'data/district_{number}/district-{number}_'
        self.colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']
        self.batteries = []
        self.houses = []
        self.load_files()
        self.connections = {battery_obj: None for battery_obj in self.batteries}
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
        orderings = list(itertools.permutations(self.batteries, 5))
        total_cost = []
        for i, battery_ordering in enumerate(orderings):
            cost = 25000 
            for battery in battery_ordering:
                distances = {house: mhd for house, mhd in self.all_distances[battery].items() if house.is_available}
                while not battery.is_full and distances:
                    house_to_add = min(distances, key=distances.get)
                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        mhd = distances.pop(house_to_add)
                        cost += mhd * 9 
                        house_to_add.is_available = False
                    else:
                        battery.is_full = True
            
            if sum([len(x) for x in self.connections.values()]) == 150:
                print()
                print("Feasible allocation found!")
                print([len(x) for x in self.connections.values()])
                print('___________________')
                print(f'Costs: {cost}')
                if i == 119:
                    self.show_connections()
            else:
                print()
                print("No feasible allocation found :(")
                print([len(x) for x in self.connections.values()])
                print('_____________________')

            total_cost.append(cost)
            self.reset_house_availability()
            self.reset_battery_capacity()
            self.reset_connections()
            
        # plt.figure()
        # plt.plot(total_cost)
        # plt.show()
        
        # if show:
        #     self.show_connections(title = 'greedy')
    
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
        plt.grid(which='major', color='#57838D', linestyle='-')
        plt.minorticks_on()
        plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
        plt.savefig(f'figures/{title}/{title.capitalize()} allocation: €{self.costs}')

    def calculate_costs(self):
        total_distance = 0
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)

if __name__ == "__main__":
    district1 = District(1)
    district1.greedy_allocation(show=True)