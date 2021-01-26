from .random import Random
from code.visualisation import visualise
from code.shared_lines import prim

import random
import copy

class HillClimber:
    '''
    The hill climber algorithm starts with a feasible solution. It then makes random swaps between houses and batteries,
    if the swap gives a more optimal solution. If no swaps are possible anymore, the algorithm comes to a stop.
    '''
    def __init__(self, algo):
        self.name = algo.name
        self.districtnumber = algo.districtnumber
        self.connections = algo.connections

    def run_unique(self, shared, save, version, k_max=100000):
        current_E = self.calculate_costs()

        for k in range(k_max):
            # make random swap
            b1, b2, h1, h2 = self.get_random_batteries()
            self.swap(b1, b2, h1, h2)
            new_E = self.update_costs(b1, b2, h1, h2)

            if not self.is_feasible():
                new_E += 500

            if new_E < current_E:
                current_E = new_E
            else:
                self.reverse_swap(b1, b2, h1, h2)
                self.update_costs(b1, b2, h2, h1)

        if shared:
            self.mst, fc = prim.create_mst(self.connections)
            self.costs = sum(fc)
            print(f"The allocation with shared lines after hill climber costs €{self.costs}")
        else:
            self.mst = None
            self.costs = current_E
            print(f"The allocation with unique lines after hill climber costs €{self.costs}")

        if version != None:
            self.version = version
        else:
            self.version = None

        if save:
            grid = visualise.Grid(self.connections, shared, self.name, self.districtnumber, self.costs, self.mst, self.version, second='hc')
    
    def run_shared(self, mst, save, version, k_max=100):

        _, current_Es = prim.create_mst(self.connections)
        current_E = sum(current_Es) 

        for k in range(k_max):
            # make random swap
            b1, b2, h1, h2 = self.get_random_batteries()
            self.swap(b1, b2, h1, h2)

            _, new_Es = prim.create_mst(self.connections)
            new_E = sum(new_Es)
            
            if not self.is_feasible():
                new_E += 500 

            if new_E < current_E:
                current_E = new_E
    
            else:
                self.reverse_swap(b1, b2, h1, h2)

        # final (global) minimum with mst
        print(f"The cost of the allocation after hill climber is €{current_E}.")
        self.costs = current_E

        if save:
            grid = visualise.Grid(self.connections, mst, self.name, self.districtnumber, self.costs, mst=None, version=None, second='hc')
    
    def get_random_batteries(self):
        random_batteries = random.sample(list(self.connections.items()), 2)
            
        batt1, houses1 = random_batteries[0]
        batt2, houses2 = random_batteries[1]

        random_house1 = random.choice(houses1)
        random_house2 = random.choice(houses2)

        return batt1, batt2, random_house1, random_house2

    def swap(self, batt1, batt2, rh1, rh2):
        self.connections[batt1].remove(rh1)
        self.connections[batt2].remove(rh2)

        self.connections[batt1].append(rh2)
        self.connections[batt2].append(rh1)

    def reverse_swap(self, batt1, batt2, rh1, rh2):
        self.connections[batt1].remove(rh2)
        self.connections[batt2].remove(rh1)

        self.connections[batt1].append(rh1)
        self.connections[batt2].append(rh2)

    def is_feasible(self):
        for battery, houses in self.connections.items():
            total_output = sum([house.output for house in houses])
            if total_output > battery.capacity:
                return False
        return True

    def get_mhd(self, battery, house):
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def calculate_costs(self):
        self.costs = 5000 * len(list(self.connections.keys()))
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)
        return self.costs

    def update_costs(self, batt1, batt2, house1, house2):
        # update costs
        self.costs -= 9 * self.get_mhd(batt1, house1)
        self.costs -= 9 * self.get_mhd(batt2, house2)
        self.costs += 9 * self.get_mhd(batt1, house2)
        self.costs += 9 * self.get_mhd(batt2, house1)

        return self.costs