import math
import random

class SimulatedAnnealing:

    def __init__(self, start_state, start_temp, k_max):
        self.connections = start_state.connections
        self.start_costs = start_state.costs
        self.start_temp = start_temp
        self.k_max = k_max
        self.counts = []

    def run(self):
        self.current_temp = self.start_temp
        self.s_old = self.calculate_costs() # oude state, specifiek de kosten van die state
        i = 0
        print(f"The starting costs in the initial state are €{self.start_costs}")
        while self.current_temp > 0.01:
            self.current_temp = self.start_temp * (0.99)**i
            # self.current_temp = self.start_temp * 1 / self.k_max
            for k in range(self.k_max):
                # maak random swap
                b1, b2, h1, h2 = self.get_random_batteries()
                self.swap(b1, b2, h1, h2)
                self.s_new = self.calculate_costs() # nieuwe state, aka de kosten van die state
                
                if not self.is_feasible():
                    self.s_new += 500 * (self.k_max / (self.k_max + 50))

                if self.acceptance_prob(self.s_old, self.s_new, self.current_temp) >= random.random():
                    self.s_old = self.s_new
                else:
                    self.reverse_swap(b1, b2, h1, h2)

                self.counts.append(self.s_old)

            if not self.is_feasible():
                print(f"The cost of this not feasible allocation is €{self.s_old}")
            else:
                print(f"This allocation is feasible and the costs are €{self.s_old}")

            if self.counts.count(self.s_old) == 50:
                print('hoi')
                break

            i += 1


    def get_temp(self, k):
        return self.T0 / math.log(k)
    
    def acceptance_prob(self, s_old, s_new, T):
        if s_new < s_old:
            return 1.0
        return math.exp((s_old - s_new) / T)

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