import matplotlib.pyplot as plt
import copy
import random
import itertools
import json

class House():
    def __init__(self, number, x, y, output):
        self.number = number
        self.x = x
        self.y = y
        self.output = output
        self.is_available = True

    #def __str__(self):
        #return f'{self.number}'
        #pass

class Battery():
    def __init__(self, number, x, y, capacity):
        self.number = number
        self.x = x
        self.y = y
        self.capacity = capacity
        self.is_full = False

    def is_feasible(self, house):
        '''Return True if battery can take given house and subtract 
        house output from battery capacity.'''
        if self.capacity - house.output < 0:
            return False
        self.capacity -= house.output
        return True

    #def __str__(self):
        #return f'{self.number}'
    #    pass

class District():
    def __init__(self, number):
        self.number = number
        self.reset_costs()
        self.path = f'data/district_{number}/district-{number}_'
        self.colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']
        self.batteries = []
        self.houses = []
        self.load_files()
        self.connections = {battery_obj: [] for battery_obj in self.batteries}
        self.battery_to_house = {battery: {house: self.get_mhd(battery, house) for house in self.houses if house.is_available} for battery in self.batteries}
        self.house_to_battery = {house: {battery: self.get_mhd(battery, house) for battery in self.batteries} for house in self.houses if house.is_available}

    def load_files(self):
        files = [self.path + 'batteries.csv', self.path + 'houses.csv']
        for filename in files:
            with open(filename, 'r') as file:
                data = file.readlines()[1:]
                for i, row in enumerate(data):
                    row = row.replace('"', '').split(',')
                    x, y, OC = int(row[0]), int(row[1]), float(row[2].rstrip())
                    if len(data) == 5:
                        self.batteries.append(Battery(i + 1, x, y, OC))
                    else:
                        self.houses.append(House(i + 1, x, y, OC))

    def random_allocation(self, show=True):
        '''
        Randomly allocates 30 houses per battery
        Repeats this process until a feasible allocation is found
        '''
        j = 0
        while not self.is_feasible():
            if j % 100 == 0:
                print(j)

            houses = copy.deepcopy(self.houses)
            random.shuffle(self.houses)
            for i, battery in enumerate(self.connections.keys()):
                self.connections[battery] = houses[i * 30: (i + 1) * 30]
            j += 1

        print("Feasible allocation found!")
        if show:
            self.show_connections(title = 'random')

    def ascending_greedy(self, show=True):
        house_output = {house: house.output for house in self.houses if house.is_available}
        while house_output:
            house_to_add = max(house_output, key=house_output.get)
            distances = {battery: mhd for battery, mhd in self.house_to_battery[house_to_add].items() if not battery.is_full if house_to_add.is_available}
            if distances:
                battery_to_connect = min(distances, key=distances.get)
                if battery_to_connect.is_feasible(house_to_add):
                    self.connections[battery_to_connect].append(house_to_add)
                    del house_output[house_to_add]
                    house_to_add.is_available = False
                else:
                    for battery in distances.keys():
                        if battery.is_feasible(house_to_add):
                            self.connections[battery].append(house_to_add)
                            del house_output[house_to_add]
                            house_to_add.is_available = False
                            break        
                    if house_to_add.is_available:
                        battery_to_connect.is_full = True

        if sum([len(x) for x in self.connections.values()]) == 150: 
            print("Feasible allocation found!")
            if show:
                self.show_connections(title='greedy2')

        self.reset_house_availability()
        self.reset_battery_capacity()
        self.reset_connections()
        self.reset_costs()
    
    def greedy_allocation(self, show=True):
        '''
        Per battery in a specific order, the closest houses are allocated 
        to that specific battery until the battery capacity is maxed out.
        Then the next battery in the order is chosen to fill up with houses.
        '''
        orderings = list(itertools.permutations(self.batteries, 5))
        for i, battery_ordering in enumerate(orderings):
            for battery in battery_ordering:
                distances = {house: mhd for house, mhd in self.battery_to_house[battery].items() if house.is_available}
                while not battery.is_full and distances:
                    house_to_add = min(distances, key=distances.get)
                    if battery.is_feasible(house_to_add):
                        self.connections[battery].append(house_to_add)
                        mhd = distances.pop(house_to_add)
                        house_to_add.is_available = False
                    else:
                        battery.is_full = True

            # if all houses are allocated, you found a feasible allocation
            if sum([len(x) for x in self.connections.values()]) == 150: 
                print("Feasible allocation found!")
                if show:
                    self.show_connections(title='greedy')
            
            self.reset_house_availability()
            self.reset_battery_capacity()
            self.reset_connections()
            self.reset_costs()
    
    def nearest_iterative(self):
        # battery capacity dictionary {battery: battery.capacity}
        battery_cap = {battery: battery.capacity for battery in self.batteries if not battery.is_full}

        for battery in self.batteries:
            #distance dictionary word gemaakt {house: mhd}
            distances = {house: mhd for house, mhd in self.battery_to_house[battery].items() if house.is_available}

        battery_to_connect = max(battery_cap, key=battery_cap.get)
        print("battery to connect:", battery_to_connect.number, "with a capacity of:", battery_to_connect.capacity)
        printnumber = 100
            
        for house, mhd in self.battery_to_house[battery_to_connect].items():
            house_to_add = min(distances, key=distances.get)
            
            if printnumber >0:
                printnumber -= 1
                print("House to add:",house_to_add.number, house_to_add.output)
                print("house_to_add.is_available:",house_to_add.is_available)
            if battery_to_connect.is_feasible(house_to_add) and house_to_add.is_available:
                print("battery_to_connect.capacity",battery_to_connect.capacity)
                print("ik ben de if statement in")
                self.connections[battery_to_connect].append(house_to_add)
                print("battery to connect en house to add:",battery_to_connect.number,house_to_add.number)
                mhd = distances.pop(house_to_add)
                house_to_add.is_available = False
            else:
                battery.is_full = True
                if printnumber >0:
                    printnumber -= 1
                    print("ik ben de else statement in")


    def ez_way(self):
        
        # matrix of lenght number of batteries of height number of houses with entries tuple of distance and boolean 
        DistanceMatrix = []
        for house in self.houses:
            DistancesPerBatterylist = []

            for battery, mhd in self.house_to_battery[house].items():
                DistancesPerBatterylist.append([mhd, False])

            DistancesPerBatterylist.insert(0,[int(house.number),round(house.output,5)])
            DistanceMatrix.append(DistancesPerBatterylist)
        
        # 0th row with battery info to be inserted into matrix for clarity
        Row0 = ["    \t"]
        for battery in self.batteries:
            Row0.append([int(battery.number),float(battery.capacity)])

        DistanceMatrix.insert(0,Row0)

        # note that [39,false] is now located at (1,1) in the array
        return DistanceMatrix
    

    def nearest_iterative_ez(self):
        DistanceMatrix = self.ez_way()
        
        i = 1
        linesegments = 0
        # for each house 1 connection
        while i < len(DistanceMatrix):
            i += 1
            
            # take the battery with the highest capacity
            Max_Cap = 0
            FirstRow = DistanceMatrix[0][1:len(DistanceMatrix[0])]
            for entry in FirstRow:
                if entry[1]>Max_Cap:
                    Max_Cap = entry[1]
                    Bat_num = entry[0]
            
            # with that battery number find the nearest house
            lowestdistance = 10000 # just has to be bigger then the other numbers
            House_num = 1
            for j in range(1,len(DistanceMatrix)):
                row = DistanceMatrix[j]
                MatrixEntry = row[Bat_num]
                distance = int(MatrixEntry[0])

                House_is_connected = False
                
                for k in range(1,len(row)):
                    Entries = row[k]
                    if Entries[1] == True:
                        House_is_connected = True
                
                if distance < lowestdistance and MatrixEntry[1] == False and House_is_connected == False:
                    lowestdistance = distance
                    House_num = row[0][0]

            # with that house number establish the connection 
            DistanceMatrix[House_num][Bat_num][1] = True
            linesegments += DistanceMatrix[House_num][Bat_num][0]

            # and lower the capacity of the battery by the apropriate amount
            House_Out = DistanceMatrix[House_num][0][1]
            if DistanceMatrix[0][Bat_num][1] == True:
                for a in DistanceMatrix:
                    for b in a:
                        print(b,end = "\t\t")
                    print()     
            DistanceMatrix[0][Bat_num][1] = round(DistanceMatrix[0][Bat_num][1] - House_Out,6)

        
        # printing for clarity
        for a in DistanceMatrix:
            for b in a:
                print(b,end = "\t\t")
            print()       

        print(linesegments)
        #self.reintegrate(DistanceMatrix)

    def reintegrate(self,DistanceMatrix):
        # over all houses and batteries
        for battery in self.batteries:
            for j in range(1,len(DistanceMatrix)):
                row = DistanceMatrix[j]
                # the specific connection in the matrix
                MatrixEntry = row[battery.number]
                boolean = MatrixEntry[1]
                if boolean:
                    house_number = MatrixEntry[0]
                    for house, mhd in self.battery_to_house[battery].items():
                        if house.number == house_number:
                            house_to_add = house
                            self.connections[battery].append(house_to_add)

    def swap(self):
        # get 2 distinct random batteries
            # get random house from each 
            # make swap
        pass

    def reset_house_availability(self):
        '''
        Resets house availability
        '''
        for house in self.houses:
            house.is_available = True
    
    def reset_battery_capacity(self):
        '''
        Resets battery capacity
        '''
        for battery in self.batteries:
            battery.capacity = round(battery.capacity + sum([house.output for house in self.connections[battery]]), 1)
            battery.is_full = False    
    
    def reset_connections(self):
        self.connections = {battery_obj: [] for battery_obj in self.batteries}
    
    def get_mhd(self, battery, house):
        '''
        Returns the manhattan distance per battery and house
        '''
        return abs(battery.x - house.x) + abs(battery.y - house.y)

    def is_feasible(self):
        '''
        Checks if total output of the houses connected to a battery
        does not exceed the battery capacity
        '''
        for battery, houses in self.connections.items():
            if not houses:
                return False
            total_output = sum([house.output for house in houses])
            if total_output > battery.capacity:
                return False
        return True
    
    def show_connections(self, title):
        '''
        Shows how the houses are connected to the batteries in a grid
        '''
        for battery, houses in self.connections.items():
            plt.scatter(battery.x, battery.y, c=self.colors[battery.number - 1], marker='s')
            for house in houses:
                plt.scatter(house.x, house.y, c=self.colors[battery.number - 1], marker='*')
                xsteps = [battery.x, house.x, house.x]
                ysteps = [battery.y, battery.y, house.y]
                plt.plot(xsteps, ysteps, c=self.colors[battery.number - 1])
        self.calculate_costs()
        plt.grid(which='major', color='#57838D', linestyle='-')
        plt.minorticks_on()
        plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
        plt.title(f"{title.capitalize()} allocation: €{self.costs}")
        plt.savefig(f'figures/{title}/{title.capitalize()} allocation: €{self.costs}')

    def calculate_costs(self):
        '''
        Calculates the cost of the allocation
        '''
        for battery, houses in self.connections.items():
            for house in houses:
                self.costs += 9 * self.get_mhd(battery, house)
    
    def reset_costs(self):
        self.costs = 25000

if __name__ == "__main__":
    district1 = District(1)
    #district1.ascending_greedy(show=True)
    #district1.random_allocation(show=True)
    #district1.nearest_iterative()
    #district1.ez_way()
    district1.nearest_iterative_ez()
    #district1.show_connections("title")
