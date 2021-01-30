from copy import deepcopy
from random import shuffle

from code.visualisation.visualise import Grid
from code.shared_lines.prim import create_mst
from output.create_output import create_output


class Random:
    def __init__(self, district):
        self.name = 'Random'
        self.districtnumber = district.number
        self.houses = deepcopy(district.houses)
        self.batteries = district.batteries
        self.connections = {battery: [] for battery in self.batteries}

    def run(self, shared, save):
        """
        Randomly allocates 30 houses per battery. 
        The algorithm repeats this process until a feasible allocation is found.
        """
        while not self.is_feasible():

            shuffle(self.houses)
            for i, battery in enumerate(self.connections.keys()):
                self.connections[battery] = self.houses[i * 30: (i + 1) * 30]

        self.feasible = True
        
        if shared:
            self.mst, fc = create_mst(self.connections)
            self.costs = sum(fc)
        else: 
            self.mst = None
            self.calculate_costs()

        print(f"Feasible allocation found! This allocation costs €{self.costs}.")
        create_output(self.name, self.districtnumber, self.costs, self.connections, shared, self.mst)

        if save:
            Grid(self.connections, shared, self.name, self.districtnumber, self.costs, self.mst, version=None)

    def is_feasible(self):
        """
        Returns true if allocation is feasible.
        """
        for battery, houses in self.connections.items():
            total_output = sum([house.output for house in houses])
            if not houses or total_output > battery.capacity:
                return False
        return True

    def calculate_costs(self):
        """
        Calculates the total costs of the allocation.
        """
        self.costs = 5000 * len(self.connections.keys())
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)

    def get_mhd(self, battery, house):
        """
        Returns the manhattan distance between battery and house.
        """
        return abs(battery.x - house.x) + abs(battery.y - house.y)