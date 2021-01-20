import copy
import random
# from code.visualisation.visualise import show_mst, show
from code.shared_lines import prim

class Random:
    '''
    Randomly allocates 30 houses per battery
    Repeats this process until a feasible allocation is found
    '''
    def __init__(self, district):
        self.name = 'Random'
        self.districtnumber = district.number
        self.houses = copy.deepcopy(district.houses)
        self.batteries = district.batteries
        self.connections = {battery: [] for battery in self.batteries}
        self.costs = 5000 * len(self.batteries)

    def run(self):
        j = 0
        while not self.is_feasible():
            if j % 100 == 0:
                print(j)

            random.shuffle(self.houses)
            for i, battery in enumerate(self.connections.keys()):
                self.connections[battery] = self.houses[i * 30: (i + 1) * 30]
            j += 1

        self.calculate_costs()
        print("Feasible allocation found!")
        # self.feasible = True
        # self.mst, fc = prim.create_mst(self.connections)
        # self.costs = sum(fc)
        # print(f"This allocation costs €{self.costs}")
        # show_mst(self)

    def is_feasible(self):
        for battery, houses in self.connections.items():
            total_output = sum([house.output for house in houses])
            if not houses or total_output > battery.capacity:
                return False
        return True

    def calculate_costs(self):
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)

    def get_mhd(self, battery, house):
        return abs(battery.x - house.x) + abs(battery.y - house.y)