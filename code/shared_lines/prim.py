from code.classes.node import Node
from copy import deepcopy
import matplotlib.pyplot as plt


def create_mst(connections):
    """
    Given an allocation between houses and batteries, this function creates a minimum spanning tree for each pair.
    It does so by finding a minimum path for each node (which can also be batteries) in the tree.
    The paths between the nodes and houses are found one by one, and so the tree grows.
    As the tree expands, the number of nodes grows as well.
    """
    forest_costs = []
    mst = {}

    for battery, houses in connections.items():
        houses = deepcopy(houses)

        # plt.scatter(battery.x, battery.y, c=battery.color, marker='s')
        # for house in houses:
        #     plt.scatter(house.x, house.y, c=battery.color, marker='*')

        costs = 5000
        mst[battery] = []

        tree = {battery: {house: get_mhd(battery, house) for house in houses}}
        
        while houses:
            ledger = []

            for from_node, distances in tree.items():
                to_node = min(distances, key=distances.get)
                ledger.append((from_node, to_node, distances[to_node]))
            
            from_node, to_node, mhd = min(ledger, key=lambda x: x[2])
            houses.remove(to_node)

            tree_nodes = list(tree.keys())
            tree = clean_tree(tree, tree_nodes, to_node)

            costs += 9 * mhd
            path = pathfinder(from_node, to_node)

            x, y = [], []
            for node in path:
                tree[node] = {house: get_mhd(node, house) for house in houses}
                x.append(node.x)
                y.append(node.y)

            mst[battery].append((x, y))
        
        forest_costs.append(costs)

        # paths = mst[battery]
        # for x, y in paths:
        #     plt.plot(x, y, c=battery.color)
        # plt.xlim([-1, 51])
        # plt.ylim([-1, 51])
        # plt.show()
            
    return mst, forest_costs

def pathfinder(from_node, to_node):
    """
    Finds a path between two nodes using the Euclidian distance heuristic, 
    and returns the respective coordinates of said path.
    """
    startnode = Node(from_node, (from_node.x, from_node.y), None, to_node)
    openlist = [startnode]
    closedlist = []

    while openlist:
        openlist = sorted(openlist, key=lambda node: node.h)
        current_node = openlist.pop(0)

        if (current_node.x, current_node.y) == (to_node.x, to_node.y):
            path_nodes = [current_node]
            node_up = current_node.parent

            while node_up is not None:
                path_nodes.append(node_up)
                node_up = node_up.parent

            for node in path_nodes:
                del node.h, node.g, node.f, node.parent

            return path_nodes

        closedlist.append(current_node)
        neighbours = get_neighbours(current_node)
        for coordinates in neighbours:
            new_node = Node(from_node, coordinates, current_node, to_node)
            if new_node in closedlist:
                continue
            if new_node not in openlist and new_node.h <= current_node.h:
                openlist.append(new_node)
    
    return None

def get_neighbours(node):
    """
    Returns the neighbors of the given node.
    """
    neighbours = []
    delta = [-1, 1]
    for i in delta:
        neighbours.append((node.x + i, node.y))
        neighbours.append((node.x, node.y + i))
    return neighbours

def clean_tree(tree, tree_nodes, to_house):
    """
    Recursively removes a node in the tree and all corresponding values in the nested dictionary.
    """
    if not tree_nodes:
        return tree
    
    node = tree_nodes.pop()
    del tree[node][to_house]

    return clean_tree(tree, tree_nodes, to_house)

def get_mhd(node1, node2):
    """
    Returns the manhattan distance between two nodes.
    """
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)