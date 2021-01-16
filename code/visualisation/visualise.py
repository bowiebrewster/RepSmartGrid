import matplotlib.pyplot as plt

def show(algorithm):
    '''
    Shows how the houses are connected to the batteries in a grid by a certain algorithm
    '''
    colors = ['#0fa2a9', '#ff1463', '#b479bb', '#15362f', '#68da23']

    for battery, houses in algorithm.connections.items():
        plt.scatter(battery.x, battery.y, c=colors[battery.number - 1], marker='s')
        for house in houses:
            plt.scatter(house.x, house.y, c=colors[battery.number - 1], marker='*')
            if algorithm.name == 'Random' or algorithm.name == 'Greedy':
                xsteps = [battery.x, house.x, house.x]
                ysteps = [battery.y, battery.y, house.y]
                plt.plot(xsteps, ysteps, c=colors[battery.number - 1])
    
    plt.grid(which='major', color='#57838D', linestyle='-')
    plt.minorticks_on()
    plt.grid(which='minor', color='#57838D', linestyle='-', alpha=0.2)
    plt.title(f"{algorithm.name} allocation: €{algorithm.costs}")
    plt.savefig(f'figures/{algorithm.name.lower()}/{algorithm.name.lower()} allocation')