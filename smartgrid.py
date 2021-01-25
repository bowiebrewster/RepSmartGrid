import matplotlib.pyplot as plt
import copy
import random
import itertools
import json

class House():
    def __init__(self, number, x, y, output):
        self.number = number
        self.x = x
        self.y = y
        self.output = output
        self.is_available = True

    def __str__(self):
        return f'{self.number}'

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
        return f'{self.number}'

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
        
        # self.connections = {}
        # for battery_obj in self.batteries:
        #     self.connections[battery_obj] = []

        self.battery_to_house = {battery: {house: self.get_mhd(battery, house) for house in self.houses if house.is_available} for battery in self.batteries}
        self.house_to_battery = {house: {battery: self.get_mhd(battery, house) for battery in self.batteries} for house in self.houses if house.is_available}

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
        '''
        Randomly allocates 30 houses per battery
        Repeats this process until a feasible allocation is found
        '''

        self.reset_house_availability()
        self.reset_battery_capacity()
        self.reset_connections()
        self.reset_costs()

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

        # print(self.connections.keys())

    def ascending_greedy(self, show=True):

        self.reset_house_availability()
        self.reset_battery_capacity()
        self.reset_connections()
        self.reset_costs()

        house_output = {house: house.output for house in self.houses if house.is_available}
        while house_output:
            house_to_add = max(house_output, key=house_output.get)
            distances = {battery: mhd for battery, mhd in self.house_to_battery[house_to_add].items() if not battery.is_full if house_to_add.is_available}
            if distances:
                battery_to_connect = min(distances, key=distances.get)
                if battery_to_connect.is_feasible(house_to_add):
                    self.connections[battery_to_connect].append(house_to_add)
                    del house_output[house_to_add]
                    house_to_add.is_available = False
                else:
                    for battery in distances.keys():
                        if battery.is_feasible(house_to_add):
                            self.connections[battery].append(house_to_add)
                            del house_output[house_to_add]
                            house_to_add.is_available = False
                            break        
                    if house_to_add.is_available:
                        battery_to_connect.is_full = True

        if sum([len(x) for x in self.connections.values()]) == 150: 
            print("Feasible allocation found!")
            if show:
                self.show_connections(title='greedy2')


    
    def greedy_allocation(self, show=True):
        '''
        Per battery in a specific order, the closest houses are allocated 
        to that specific battery until the battery capacity is maxed out.
        Then the next battery in the order is chosen to fill up with houses.
        '''

        self.reset_house_availability()
        self.reset_battery_capacity()
        self.reset_connections()
        self.reset_costs()

        orderings = list(itertools.permutations(self.batteries, 5))
        for i, battery_ordering in enumerate(orderings):
            for battery in battery_ordering:
                distances = {house: mhd for house, mhd in self.battery_to_house[battery].items() if house.is_available}

                while not battery.is_full and distances:
                    house_to_add = min(distances, key=distances.get)
                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        mhd = distances.pop(house_to_add)
                        house_to_add.is_available = False
                    else:
                        battery.is_full = True

            # if all houses are allocated, you found a feasible allocation
            if sum([len(x) for x in self.connections.values()]) == 150: 
                print("Feasible allocation found!")
                if show:
                    self.show_connections(title='greedy')
            
            print(self.connections.items())
            
    
    def simulated_annealing(self):
        # count costs before swap # old_cost = self.calculate_costs()
# for battery, houses in 
# self.connections[battery]
        # get two distinct random batteries
            # get random house from the two batteries
                # make feasible swap with these houses
                # count costs after swap # new_cost = self.calculate_costs()
                # if new_costs < old_cost:
                    # save this change # best_cost = new_cost
                # else:
                    # swap the houses back
        
        # get a random item in dictionary
        # a_dict = {'a': 1, 'b': 2, 'c': 3}
        # entry_list = list(a_dict.items())
        # random_entry = random.choice(entry_list)
        # print(random_entry) -> output = ('b', 2)

# SIMULATED ANNEALING PSEUDO CODE SLIDES:
# Herhaal:
#     Kies een random start state
#     Kies start temperatuur
#     Herhaal N iteraties:
#         Doe een kleine random aanpassing
#         Als random() > kans(oud, nieuw, temperatuur):
#             Maak de aanpassing ongedaan
#         Verlaag temperatuur

        pass

    def reset_house_availability(self):
        '''
        Resets house availability
        '''
        for house in self.houses:
            house.is_available = True
    
    def reset_battery_capacity(self):
        '''
        Resets battery capacity
        '''
        for battery in self.batteries:
            battery.capacity = round(battery.capacity + sum([house.output for house in self.connections[battery]]), 1)
            battery.is_full = False    
    
    def reset_connections(self):
        self.connections = {battery_obj: [] for battery_obj in self.batteries}
    
    def get_mhd(self, battery, house):
        '''
        Returns the manhattan distance per battery and house
        '''
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def is_feasible(self):
        '''
        Checks if total output of the houses connected to a battery
        does not exceed the battery capacity
        '''
        for battery, houses in self.connections.items():
            if not houses:
                return False
            total_output = sum([house.output for house in houses])
            if total_output > battery.capacity:
                return False
        return True
    
    def show_connections(self, title):
        '''
        Shows how the houses are connected to the batteries in a grid
        '''
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
        plt.title(f"{title.capitalize()} allocation: €{self.costs}")
        plt.savefig(f'figures/{title}/{title.capitalize()} allocation -- €{self.costs}')

    def calculate_costs(self):
        '''
        Calculates the cost of the allocation
        '''
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)
    
    def reset_costs(self):
        self.costs = 25000

if __name__ == "__main__":
    district1 = District(1)
    district2 = District(2)
    district3 = District(3)

    district1.ascending_greedy(show=True)
    # district2.random_allocation(show=True)
    # district2.greedy_allocation(show=True)