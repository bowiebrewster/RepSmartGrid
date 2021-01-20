from .random import Random

import random
import copy

class HillClimber:
    '''
    The hill climber algorithm starts with a random feasible solution. It then makes random swaps between houses and batteries,
    if the swap gives a more optimal solution. If no swaps are possible anymore, the algorithm comes to a stop.
    '''
    def __init__(self, district):
        self.name = 'Hill Climber'
        self.district = district
        self.houses = district.houses
        self.batteries = district.batteries

    def random_allocation(self):
        allocation = Random(self.district)
        allocation.run()
        self.costs = allocation.costs
        self.connections = allocation.connections

    def random_swap(self):
        batt1, batt2, idx1, idx2 = self.get_random_houses()
        while batt1 == batt2 and idx1 == idx2:
            batt1, batt2, idx1, idx2 = self.get_random_houses()
        house1 = self.connections[batt1].pop(idx1)
        house2 = self.connections[batt2].pop(idx2)
        self.connections[batt1] = house2
        self.connections[batt2] = house1

        if allocation.is_feasible():
            if allocation.calculate_costs() < self.costs:
                # save this swap
                continue
            else:
                # undo this swap
                self.connections[batt1], self.connections[batt2] = self.connections[batt2], self.connections[batt1]

    def get_random_houses(self):
        batt1 = random.choice(list(self.connections.keys()))
        batt2 = random.choice(list(self.connections.keys()))
        idx1 = random.randint(0, len(self.connections[batt1]))
        idx2 = random.randint(0, len(self.connections[batt2]))
        return batt1, batt2, idx1, idx2