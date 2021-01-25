import math
import random

class SimulatedAnnealing:

    def __init__(self, start_state, start_temp, n):
        self.connections = start_state.connections
        self.start_costs = start_state.costs
        self.start_temp = start_temp
        self.n = n
        self.fine = 0

    def run(self):
        print(f"The starting costs in the initial state are {self.start_costs}")
        self.old_costs = self.start_costs
        self.current_temp = self.start_temp

        # Herhaal n iteraties
        for i in range(0, self.n):
            # print(f"We zitten nu in iteratie {i} vd for loop")

            # Doe een kleine random aanpassing
            batt1, batt2, rh1, rh2 = self.get_random_batteries()

            self.swap(batt1, batt2, rh1, rh2)
            self.calculate_costs()

            if not self.is_feasible():
                self.fine += 10000
            
            # Als random() > kans(oud, nieuw, temperatuur):
            if random.random() > self.acceptance_probability(self.old_costs, self.new_costs, self.current_temp):
                # Maak de aanpassing ongedaan
                self.reverse_swap(batt1, batt2, rh1, rh2)
            else:
                # update oude en nieuwe kosten
                self.old_costs = self.new_costs
        
            # Verlaag temperatuur
            self.current_temp = (self.current_temp)**i
            # self.current_temp = (self.start_temp)**i # staat in de slides??

        # print(self.current_temp)

        print(f"The costs after SA are {self.new_costs}")

    def acceptance_probability(self, old_cost, new_cost, temp):
        if new_cost < old_cost:
            return 1.0
        else:
            return math.exp((old_cost - new_cost) / temp)

    def penalty(self):
        if not self.is_feasible():
            self.new_costs += 10000
            return True
        return False

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
        for battery, houses in self.connections.items():
            for house in houses:
                try:
                    self.new_costs += 9 * self.get_mhd(battery, house)
                except:
                    self.new_costs = 9 * self.get_mhd(battery, house)