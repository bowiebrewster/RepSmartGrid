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
    
    def run_v1(self, shared, save):
        '''
        Per battery in a specific order, the closest houses are allocated 
        to that specific battery until the battery capacity is maxed out.
        Then the next battery in the order is chosen to fill up with houses.
        '''

        all_allocations = {}

        self.version = 1

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

            if self.feasible_allocation():

                print("Feasible allocation found!")

                if shared:
                    self.mst, fc = prim.create_mst(self.connections)
                    self.costs = sum(fc)
                else:
                    self.mst = None

                print(f"This allocation costs €{self.costs}.")

                connections = copy.deepcopy(self.connections)
                all_allocations[self.costs] = connections

                if save:
                    grid = visualise.Grid(self.connections, shared, self.name, self.districtnumber, self.costs, self.mst, self.version)
                
            self.reset()
        
        # we move forward with the smallest cost
        try:
            self.costs, self.connections = min(all_allocations.items(), key=lambda x: x[0])
            self.feasible = True
        except:
            self.feasible = False

    def run_v2(self, shared, save):
        self.version = 2

        for i in range(len(self.houses)):
            house_output = {house: house.output for house in self.houses if house.is_available}
            house_to_add = max(house_output, key=house_output.get)
            distances = self.batteries_distances(house_to_add)
            battery_to_connect = min(distances, key=distances.get)
            
            if battery_to_connect.is_feasible(house_to_add):
                self.connections[battery_to_connect].append(house_to_add)
                house_to_add.is_available = False
                mhd = distances[battery_to_connect]
                self.costs += 9 * mhd
            else:
                for battery in self.batteries:
                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        house_to_add.is_available = False
                        mhd = distances[battery]
                        self.costs += 9 * mhd
                        break

        if self.feasible_allocation():
            self.feasible = True
            print("Feasible allocation found!")

            if shared:
                self.mst, fc = prim.create_mst(self.connections)
                self.costs = sum(fc)
            else:
                self.mst = None

            print(f"This allocation costs €{self.costs}")

            if save:
                grid = visualise.Grid(self.connections, shared, self.name, self.districtnumber, self.costs, self.mst, self.version)
        else:
            self.feasible = False

    def feasible_allocation(self):
        if sum([len(x) for x in self.connections.values()]) == 150: 
            return True
        return False

    def swap(self):
        # get 2 distinct random batteries
        # get random house from each 
        # make swap
        pass

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