import itertools
import random
import copy
import matplotlib.pyplot as plt
from code.visualisation import visualise
from code.shared_lines import prim

class Greedy:
    '''
    The Greedy class that assigns the best possible house to each battery one by one.
    '''
    def __init__(self, district):
        self.name = 'Greedy'
        self.districtnumber = district.number
        self.batteries = district.batteries
        self.houses = district.houses
        self.connections = {battery: [] for battery in self.batteries}
        self.reset()
    
    def houses_distances(self, battery):
        return {house: self.get_mhd(battery, house) for house in self.houses if house.is_available}

    def batteries_distances(self, house):
        return {battery: self.get_mhd(battery, house) for battery in self.batteries if not battery.is_full}
    
    def run_v1(self, mst, save):
        '''
        Per battery in a specific order, the closest houses are allocated 
        to that specific battery until the battery capacity is maxed out.
        Then the next battery in the order is chosen to fill up with houses.
        '''

        self.version = 1
        print("Let's get version 1 running!")

        orderings = list(itertools.permutations(self.batteries, 5))
        for i, battery_ordering in enumerate(orderings):
            for battery in battery_ordering:
                distances = self.houses_distances(battery)

                while not battery.is_full and distances:
                    house_to_add = min(distances, key=distances.get)

                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        self.costs += 9 * distances.pop(house_to_add)
                        house_to_add.is_available = False
                    else:
                        battery.is_full = True

            if self.feasible_allocation() and i == 118:
                print("Feasible allocation found!")
                if save:
                    if mst:
                        self.mst, fc = prim.create_mst(self.connections)
                        self.costs = sum(fc)
                    else: 
                        self.calculate_costs()

                    print(f"This allocation costs €{self.costs}")
                    grid = visualise.Grid(self.connections, mst, self.name, self.districtnumber, self.costs, self.version)
                
            self.reset()

    def run_v2(self, mst, save):
        self.version = 2
        print("Let's get version 2 running!")
        house_output = {house: house.output for house in self.houses if house.is_available}

        i = 0
        while house_output and i <= 150:
            if i % 10 ==0:
                print(i)

            house_to_add = max(house_output, key=house_output.get)
            distances = self.batteries_distances(house_to_add)

            if distances:
                battery_to_connect = min(distances, key=distances.get)
                if battery_to_connect.is_feasible(house_to_add):
                    self.connections[battery_to_connect].append(house_to_add)
                    del house_output[house_to_add]
                    mhd = distances.pop(battery_to_connect)
                    self.costs += 9 * mhd
                else:
                    for battery in distances.keys():
                        if battery.is_feasible(house_to_add):
                            self.connections[battery].append(house_to_add)
                            self.costs += 9 * distances[battery_to_connect]
                            del house_output[house_to_add]
                            house_to_add.is_available = False
                            break  
                        else:
                            battery_to_connect.is_full = True
            i += 1

        if self.feasible_allocation():
            print("Feasible allocation found!")
            if save:
                if mst:
                    self.mst, fc = prim.create_mst(self.connections)
                    self.costs = sum(fc)
                else: 
                    self.calculate_costs()

                print(f"This allocation costs €{self.costs}")
                grid = visualise.Grid(self.connections, mst, self.name, self.districtnumber, self.costs, self.version)
        else:
            print("No feasible allocation found :(")

    def feasible_allocation(self):
        if sum([len(x) for x in self.connections.values()]) == 150: 
            return True
        return False

    def reset(self):
        self.costs = 5000 * len(self.batteries)

        for house in self.houses:
            house.is_available = True
        
        for battery in self.batteries:
            battery.capacity = round(battery.capacity + sum([house.output for house in self.connections[battery]]), 1)
            battery.is_full = False

        self.connections = {battery: [] for battery in self.batteries}

    def get_mhd(self, battery, house):
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def calculate_costs(self):
        self.costs = 5000 * len(list(self.connections.keys()))
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)
        return self.costs