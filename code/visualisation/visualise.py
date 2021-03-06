import matplotlib.pyplot as plt

class Grid:
    def __init__(self, connections, shared, name, number, costs, mst, version, second=None):
        self.connections = connections
        self.shared = shared
        self.name = name
        self.version = version
        self.number = number
        self.costs = costs
        self.load_grid()
        self.second = second
      
        if self.shared:
            self.mst = mst
            self.show_shared()
        else:
            self.show_unique()

    def load_grid(self):
        for battery, houses in self.connections.items():
            plt.scatter(battery.x, battery.y, c=battery.color, marker='s')
            for house in houses:
                plt.scatter(house.x, house.y, c=battery.color, marker='*')

        plt.grid(which='major', color='#57838D', linestyle='-')
        plt.minorticks_on()
        plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)

    def show_unique(self):
        for battery, houses in self.connections.items():
            for house in houses:
                xsteps = [battery.x, house.x, house.x]
                ysteps = [battery.y, battery.y, house.y]
                plt.plot(xsteps, ysteps, c=battery.color)

        plt.title(f"District {self.number} allocation €{self.costs}")

        if self.second != None:
            if self.version != None:
                plt.savefig(f'figures/{self.name.lower()}/version_{self.version}/unique/{self.second}/District {self.number} allocation €{self.costs}')
            else:
                plt.savefig(f'figures/{self.name.lower()}/unique/{self.second}/District {self.number} allocation €{self.costs}')
        else:
            if self.version != None:
                plt.savefig(f'figures/{self.name.lower()}/version_{self.version}/unique/District {self.number} allocation €{self.costs}')
            else:
                plt.savefig(f'figures/{self.name.lower()}/unique/District {self.number} allocation €{self.costs}')

        plt.close()

    def show_shared(self):
        for battery in self.connections.keys():
            paths = self.mst[battery]
            for x, y in paths:
                plt.plot(x, y, c=battery.color)
        
        plt.title(f"District {self.number} allocation €{self.costs}")
        
        if self.second != None:
            if self.version != None:
                plt.savefig(f'figures/{self.name.lower()}/version_{self.version}/shared/{self.second}/District {self.number} allocation €{self.costs}')
            else:
                plt.savefig(f'figures/{self.name.lower()}/shared/{self.second}/District {self.number} allocation €{self.costs}')
        else:
            if self.version != None:
                plt.savefig(f'figures/{self.name.lower()}/version_{self.version}/shared/District {self.number} allocation €{self.costs}')
            else:
                plt.savefig(f'figures/{self.name.lower()}/shared/District {self.number} allocation €{self.costs}')
        
        plt.close()