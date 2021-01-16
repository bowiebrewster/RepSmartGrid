import itertools, math

class Node:
    
    number = itertools.count()

    def __init__(self, start_node, coordinates, parent, target_node):
        self.idnr = next(Node.number)
        self.x, self.y = coordinates
        self.parent = parent
        self.g = abs(start_node.x - self. x) + abs(start_node.y - self.y)
        self.h = (self.x - target_node.x)**2 + (self.y - target_node.y)**2
        self.f = self.h + self.g