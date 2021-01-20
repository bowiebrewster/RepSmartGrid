import matplotlib.pyplot as plt

def show_sa(algorithm):
    '''
    Shows how the houses are connected to the batteries in a grid by a certain algorithm
    '''

    colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']

    for battery, houses in algorithm.connections.items():
        plt.scatter(battery.x, battery.y, c=colors[battery.number - 1], marker='s')
        for house in houses:
            plt.scatter(house.x, house.y, c=colors[battery.number - 1], marker='*')

            xsteps = [battery.x, house.x, house.x]
            ysteps = [battery.y, battery.y, house.y]
            plt.plot(xsteps, ysteps, c=colors[battery.number - 1])

    plt.grid(which='major', color='#57838D', linestyle='-')
    plt.minorticks_on()
    plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
    plt.title(f"District {algorithm.districtnumber} {algorithm.name} allocation after SA: €{algorithm.costs}")
    plt.savefig(f'figures/sa/district_{algorithm.districtnumber}/{algorithm.name} allocation after SA €{algorithm.costs}')

def show_r(algorithm):
    '''
    Shows how the houses are connected to the batteries in a grid by a certain algorithm
    '''

    colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']

    for battery, houses in algorithm.connections.items():
        plt.scatter(battery.x, battery.y, c=colors[battery.number - 1], marker='s')
        for house in houses:
            plt.scatter(house.x, house.y, c=colors[battery.number - 1], marker='*')

            xsteps = [battery.x, house.x, house.x]
            ysteps = [battery.y, battery.y, house.y]
            plt.plot(xsteps, ysteps, c=colors[battery.number - 1])

    plt.grid(which='major', color='#57838D', linestyle='-')
    plt.minorticks_on()
    plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
    plt.title(f"District {algorithm.districtnumber} {algorithm.name} allocation before SA: €{algorithm.costs}")
    plt.savefig(f'figures/sa/district_{algorithm.districtnumber}/{algorithm.name} allocation before SA €{algorithm.costs}')

def show_mst(algorithm):
    for battery, houses in algorithm.connections.items():
        plt.scatter(battery.x, battery.y, c=battery.color, marker='H')
        for house in houses:
            plt.scatter(house.x, house.y, c=battery.color, marker='*')
        paths = algorithm.mst[battery]
        for x, y in paths:
            plt.plot(x, y, c=battery.color)
    
    plt.grid(which='major', color='#57838D', linestyle='-')
    plt.minorticks_on()
    plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
    plt.title(f"Minimum spanning tree - Random allocation: €{algorithm.costs}")
    plt.savefig(f'figures/mst/district_{algorithm.districtnumber}/{algorithm.name} allocation €{algorithm.costs}')