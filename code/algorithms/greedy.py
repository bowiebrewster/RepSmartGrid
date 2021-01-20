import itertools
import random
import copy
import matplotlib.pyplot as plt
from code.visualisation.visualise import show_mst
from code.shared_lines import prim

class Greedy:
    '''
    The Greedy class that assigns the best possible house to each battery one by one.
    '''
    def __init__(self, district):
        self.name = 'Greedy'
        self.districtnumber = district.number
        self.batteries = district.batteries
        self.houses = district.houses
        self.connections = {battery: [] for battery in self.batteries}
        # self.colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']
        self.reset()
    
    def get_distances_battery_to_house(self, battery):
        return {house: self.get_mhd(battery, house) for house in self.houses if house.is_available}

    def get_distances_house_to_battery(self, house):
        return {battery: self.get_mhd(battery, house) for battery in self.batteries if not battery.is_full}
    
    def run_v1(self):
        '''
        Per battery in a specific order, the closest houses are allocated 
        to that specific battery until the battery capacity is maxed out.
        Then the next battery in the order is chosen to fill up with houses.
        '''
        orderings = list(itertools.permutations(self.batteries, 5))
        for i, battery_ordering in enumerate(orderings):
            for battery in battery_ordering:
                distances = self.get_distances_battery_to_house(battery)

                while not battery.is_full and distances:
                    house_to_add = min(distances, key=distances.get)

                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        self.costs += 9 * distances.pop(house_to_add)
                        house_to_add.is_available = False
                    else:
                        battery.is_full = True

            if self.feasible_allocation() and i == 118:
                print("Feasible allocation found!")
                break
                # self.feasible = True
                # self.mst, fc = prim.create_mst(self.connections)
                # self.costs = sum(fc)
                # print(f"This allocation costs €{self.costs}")
            #     # show_mst(self)
            # else:
            #     self.feasible = False
                
            self.reset()

    def run_v2(self):
        house_output = {house: house.output for house in self.houses if house.is_available}
        i = 0
        while house_output:

            house_to_add = max(house_output, key=house_output.get)
            distances = self.get_distances_house_to_battery(house_to_add)

            if distances:
                battery_to_connect = min(distances, key=distances.get)
                if battery_to_connect.is_feasible(house_to_add):
                    self.connections[battery_to_connect].append(house_to_add)
                    del house_output[house_to_add]
                    mhd = distances.pop(battery_to_connect)
                    self.costs += 9 * mhd
                else:
                    for battery in distances.keys():
                        if battery.is_feasible(house_to_add):
                            self.connections[battery].append(house_to_add)
                            self.costs += 9 * distances[battery_to_connect]
                            del house_output[house_to_add]
                            house_to_add.is_available = False
                            break  
                        else:
                            battery_to_connect.is_full = True
            i += 1
            if i == 150:
                if self.feasible_allocation():
                    print("Feasible allocation found!")
                    self.mst, fc = prim.create_mst(self.connections)
                    self.costs = sum(fc)
                    print(f"This allocation costs €{self.costs}")
                    show_mst(self)
                    self.feasible = True
                else:
                    print("No feasible allocation found :(")
                    self.feasible = False
                break

    def show(self):
        for battery, houses in self.connections.items():
            plt.scatter(battery.x, battery.y, c=self.colors[battery.number - 1], marker='s')
            for house in houses:
                plt.scatter(house.x, house.y, c=self.colors[battery.number - 1], marker='*')

                xsteps = [battery.x, house.x, house.x]
                ysteps = [battery.y, battery.y, house.y]
                plt.plot(xsteps, ysteps, c=self.colors[battery.number - 1])

        plt.grid(which='major', color='#57838D', linestyle='-')
        plt.minorticks_on()
        plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
        plt.title(f"{self.name} allocation: €{self.costs}")
        plt.savefig(f'figures/{self.name.lower()}/District {self.districtnumber}: {self.name} allocation €{self.costs}')

    def feasible_allocation(self):
        if sum([len(x) for x in self.connections.values()]) == 150: 
            return True
        return False

    def swap(self):
        # get 2 distinct random batteries
        # get random house from each 
        # make swap
        pass

    def reset(self):
        self.costs = 5000 * len(self.batteries)

        for house in self.houses:
            house.is_available = True
        
        for battery in self.batteries:
            battery.capacity = round(battery.capacity + sum([house.output for house in self.connections[battery]]), 1)
            battery.is_full = False

        self.connections = {battery: [] for battery in self.batteries}

    def get_mhd(self, battery, house):
        return abs(battery.x - house.x) + abs(battery.y - house.y)