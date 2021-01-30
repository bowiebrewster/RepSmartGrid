from itertools import permutations

from code.visualisation.visualise import Grid
from code.shared_lines.prim import create_mst
from output.create_output import create_output


class Greedy:
    def __init__(self, district):
        self.name = 'Greedy'
        self.districtnumber = district.number
        self.batteries = district.batteries
        self.houses = district.houses
        self.connections = {battery: [] for battery in self.batteries}
        self.reset()
    
    def run_v1(self, shared, save):
        """
        Per battery in a specific order, the algorithm chooses the closest houses to connect until the battery is full.
        """
        self.version = 1
        self.feasible = False

        orderings = list(permutations(self.batteries, 5))
        for i, battery_ordering in enumerate(orderings):
            for battery in battery_ordering:
                distances = self.houses_distances(battery)

                while not battery.is_full and distances:
                    house_to_add = min(distances, key=distances.get)

                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        self.costs += 9 * distances.pop(house_to_add)
                        house_to_add.is_available = False
                    else:
                        battery.is_full = True

            if self.feasible_allocation() and i == 119:
                self.feasible = True

                if shared:
                    self.mst, fc = create_mst(self.connections)
                    self.costs = sum(fc)
                else:
                    self.mst = None

                print(f"Feasible allocation found! This allocation costs €{self.costs}.")
                create_output(self.name, self.districtnumber, self.costs, self.connections, shared, self.mst)

                if save:
                    Grid(self.connections, shared, self.name, self.districtnumber, self.costs, self.mst, self.version)

                break
                
            self.reset()

    def run_v2(self, shared, save):
        """
        With each iteration, the house with the largest output is selected and if possible, connected to the closest battery.
        """
        self.version = 2
        self.feasible = False

        for i in range(len(self.houses)):
            house_output = {house: house.output for house in self.houses if house.is_available}
            house_to_add = max(house_output, key=house_output.get)
            distances = self.batteries_distances(house_to_add)
            battery_to_connect = min(distances, key=distances.get)
            
            if battery_to_connect.is_feasible(house_to_add):
                self.connections[battery_to_connect].append(house_to_add)
                house_to_add.is_available = False
                mhd = distances[battery_to_connect]
                self.costs += 9 * mhd
            else:
                for battery in self.batteries:
                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        house_to_add.is_available = False
                        mhd = distances[battery]
                        self.costs += 9 * mhd
                        break

        if self.feasible_allocation():
            self.feasible = True

            if shared:
                self.mst, fc = create_mst(self.connections)
                self.costs = sum(fc)
            else:
                self.mst = None

            print(f"Feasible allocation found! This allocation costs €{self.costs}")
            create_output(self.name, self.districtnumber, self.costs, self.connections, shared, self.mst)

            if save:
                Grid(self.connections, shared, self.name, self.districtnumber, self.costs, self.mst, self.version)

    def feasible_allocation(self):
        """
        Returns true if all 150 houses are allocated to batteries
        """
        if sum([len(x) for x in self.connections.values()]) == 150: 
            return True
        return False

    def reset(self):
        """
        Resets costs, house availability, battery capacity and connections.
        """
        self.costs = 5000 * len(self.batteries)

        for house in self.houses:
            house.is_available = True
        
        for battery in self.batteries:
            battery.capacity = round(battery.capacity + sum([house.output for house in self.connections[battery]]), 1)
            battery.is_full = False

        self.connections = {battery: [] for battery in self.batteries}

    def get_mhd(self, battery, house):
        """
        Returns the manhattan distance between battery and house.
        """
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def houses_distances(self, battery):
        """
        Returns a dictionary with key house object and value the manhattan distances between each house and the given battery.
        """
        return {house: self.get_mhd(battery, house) for house in self.houses if house.is_available}

    def batteries_distances(self, house):
        """
        Returns a dictionary with key battery object and value the manhattan distances between each battery and the given house.
        """
        return {battery: self.get_mhd(battery, house) for battery in self.batteries if not battery.is_full}