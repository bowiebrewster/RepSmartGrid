import math
import random
import time
from code.visualisation import visualise
from code.shared_lines import prim

class SimulatedAnnealing:

    def __init__(self, algo, start_temp=None, k_max=None):
        self.connections = algo.connections
        self.districtnumber = algo.districtnumber
        self.name = algo.name

    def run_unique(self, cr, start_temp, mst, save, k_max=50):
        current_temp = start_temp
        current_E = self.calculate_costs()

        i = 0
        while current_temp > 0.001:

            if current_temp < 0:
                break

            current_temp = start_temp * (1 - cr)**i # exponential

            for k in range(k_max):
                # make random swap
                b1, b2, h1, h2 = self.get_random_batteries()
                self.swap(b1, b2, h1, h2)
                new_E = self.calculate_costs()

                if not self.is_feasible():
                    new_E += 500

                if self.acceptance_prob(current_E, new_E, current_temp) >= random.random():
                    current_E = new_E
                else:
                    self.reverse_swap(b1, b2, h1, h2)
            i += 1
            print(f"The cost is now €{current_E}")

        # final (global) minimum without mst
        print(f"The allocation after simulated annealing costs €{current_E}")
        # self.costs = current_E

        if save:
            self.mst, fc = prim.create_mst(self.connections)
            self.costs = sum(fc)
            print(f"The allocation with MST costs €{self.costs}")
            grid = visualise.Grid(self.connections, True, self.name, self.districtnumber, self.costs, self.mst, version=None, second='sa')
    
    def run_shared(self, cr, start_temp, mst, save, k_max=100):
        f = open("testing.txt", "a")

        current_temp = start_temp

        _, current_Es = prim.create_mst(self.connections)
        current_E = sum(current_Es) 
        
        i = 0

        while current_temp > 0.02:
            current_temp = start_temp * (1 - cr)**i
            # current_temp -= cr

            if current_temp < 0.02:
                break

            for k in range(k_max):
                # make random swap
                b1, b2, h1, h2 = self.get_random_batteries()
                self.swap(b1, b2, h1, h2)

                _, new_Es = prim.create_mst(self.connections)
                new_E = sum(new_Es)
                
                if not self.is_feasible():
                    new_E += 500 

                if self.acceptance_prob(current_E, new_E, current_temp) >= random.random():
                    current_E = new_E
        
                else:
                    self.reverse_swap(b1, b2, h1, h2)

            i += 1

            print(f"The cost is now €{current_E}")
            f.write(f"{current_E}\n")

        f.close()

        # final (global) minimum with mst
        print(f"The allocation after simulated annealing costs €{current_E}")
        self.costs = current_E
        self.mst, _ = prim.create_mst(self.connections)

        if save:
            grid = visualise.Grid(self.connections, mst, self.name, self.districtnumber, self.costs, self.mst, version=None, second='sa')

    def get_temp(self, k):
        return self.T0 / math.log(k)
    
    def acceptance_prob(self, current_E, new_E, T):
        if new_E < current_E:
            return 1.0
        return math.exp((current_E - new_E) / T)

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