from .random import Random

import random
import copy

class HillClimber:
    '''
    The hill climber algorithm starts with a random feasible solution. It then makes random swaps between houses and batteries,
    if the swap gives a more optimal solution. If no swaps are possible anymore, the algorithm comes to a stop.
    '''
    def __init__(self, algo):
        self.name = 'Hill Climber'
        self.districtnumber = algo.districtnumber
        self.connections = algo.connections

    def run_unique(self, k_max=100):
        current_E = self.calculate_costs()

        for k in range(k_max):
            # make random swap
            b1, b2, h1, h2 = self.get_random_batteries()
            self.swap(b1, b2, h1, h2)
            new_E = self.calculate_costs()

            if not self.is_feasible():
                new_E += 500

            if new_E < current_E:
                current_E = new_E
            else:
                self.reverse_swap(b1, b2, h1, h2)

        # final (global) minimum without mst
        print(f"The cost of the allocation after hill climber is €{current_E}.")
    
    def run_shared(self, k_max=10):

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