import math
import random


class HillClimber:
    """
    HILL CLIMBER PSEUDO SLIDES:
    Kies een random start state
    Herhaal n keer: OF Herhaal tot na n keer niet meer verbeterd:
        Doe een kleine random aanpassing
        Als de state verslechterd: 
            Maak de aanpassing ongedaan
    """

    def __init__(self, start_state):
        self.connections = start_state.connections
        self.start_costs = start_state.costs
        self.districtnumber = start_state.districtnumber
        self.name = 'Hill Climber'

    def run_unique(self):
        # de kosten van de oude state zijn op dit moment ook de beste kosten, er valt nog niks te vergelijken
        self.best_costs = self.calculate_costs() 

        print(f"The starting costs in the initial state are €{self.start_costs}")

        count_verslechtering = 0
        # als er 50 (kan nog aangepast worden) keer een verslechtering is, dan stopt het algoritme met runnen
        while count_verslechtering != 50:

            # maak random swap
            b1, b2, h1, h2 = self.get_random_houses()
            self.swap(b1, b2, h1, h2)

            # bereken de kosten van de nieuwe state
            self.new_costs = self.calculate_costs() 

            # bewaar de nieuwe kosten als beste kosten als de state verbeterd
            if self.new_costs < self.best_costs:
                self.best_costs = self.new_costs
                # aantal aansluitende verslechteringen wordt gereset
                count_verslechtering = 0
            # maak swap ongedaan als de state verslechterd
            else:
                self.reverse_swap(b1, b2, h1, h2)
                # aantal aansluitende verslechteringen gaat met 1 omhoog
                count_verslechtering += 1

        self.costs = self.best_costs

    def get_random_houses(self):
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