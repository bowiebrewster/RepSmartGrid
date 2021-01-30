from random import sample, choice

from code.visualisation.visualise import Grid
from code.shared_lines.prim import create_mst
from output.create_output import create_output


class HillClimber:
    def __init__(self, algo):
        self.name = algo.name
        self.districtnumber = algo.districtnumber
        self.connections = algo.connections
        self.calculate_costs()

    def run(self, shared, save, version):
        """
        The hill climber algorithm starts with a feasible solution. It then makes random swaps between houses and batteries,
        if the swap gives a more optimal solution. 
        """
        k_max = 100000
        current_E = self.costs

        for k in range(k_max):
            
            b1, b2, h1, h2 = self.get_random_batteries()
            self.swap(b1, b2, h1, h2)
            new_E = self.update_costs(b1, b2, h1, h2)

            if not self.is_feasible():
                new_E += 500

            if new_E < current_E:
                current_E = new_E
            else:
                self.swap(b1, b2, h2, h1)
                self.update_costs(b1, b2, h2, h1)

        if shared:
            self.mst, fc = create_mst(self.connections)
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

        create_output('HC', self.districtnumber, self.costs, self.connections, shared, self.mst)

        if save:
            Grid(self.connections, shared, self.name, self.districtnumber, self.costs, self.mst, self.version, second='hc')

    def is_feasible(self):
        """
        Returns true if allocation is feasible.
        """
        for battery, houses in self.connections.items():
            total_output = sum([house.output for house in houses])
            if total_output > battery.capacity:
                return False
        return True

    def calculate_costs(self):
        """
        Calculates the total costs of the allocation.
        """
        self.costs = 5000 * len(list(self.connections.keys()))
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)

    def update_costs(self, b1, b2, h1, h2):
        """
        Updates the total costs after swapping two houses.
        """
        self.costs -= 9 * self.get_mhd(b1, h1)
        self.costs -= 9 * self.get_mhd(b2, h2)
        self.costs += 9 * self.get_mhd(b1, h2)
        self.costs += 9 * self.get_mhd(b2, h1)

        return self.costs

    def get_mhd(self, battery, house):
        """
        Returns the manhattan distance between battery and house.
        """
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def get_random_batteries(self):
        """
        Returns two random batteries and two random houses.
        """
        random_batteries = sample(list(self.connections.items()), 2)
            
        b1, hs1 = random_batteries[0]
        b2, hs2 = random_batteries[1]

        h1 = choice(hs1)
        h2 = choice(hs2)

        return b1, b2, h1, h2

    def swap(self, b1, b2, h1, h2):
        """
        Swaps two houses given their connection to two batteries.
        """
        self.connections[b1].remove(h1)
        self.connections[b2].remove(h2)

        self.connections[b1].append(h2)
        self.connections[b2].append(h1)