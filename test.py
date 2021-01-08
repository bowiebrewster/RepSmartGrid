import matplotlib.pyplot as plt
import random
import copy
import numpy as np
import operator
import collections

# path = f'data/district_1/district-1_'
# files = [path + 'batteries.csv', path + 'houses.csv'] # de twee bestanden opslaan in lijst
# for filename in files:
#     with open(filename, 'r') as file:
#         data = file.readlines()[1:]
#         # per regel check welke elementen de coordinaten zijn en welke de output/capacity
#         for i, row in enumerate(data):
#             row = row.replace('"', '').split(',')
#             print(i)
#             print(row)

# connections = {i: None for i in range(1, 6)}
# houses = list(range(1, 151))
# random.shuffle(houses)
# for i, battery in enumerate(connections.keys()):
#     connections[battery] = houses[i * 30: (i + 1) * 30]
# print(connections)

a = list(range(1, 151))
houses = [(1, 1), (2, 3), (4, 10)]
battery = (5, 6)
distances = {}
for house in houses:
    manhattan_distance = abs(battery[0] - house[0]) + abs(battery[1] - house[1])
    distances[house] = manhattan_distance

sorted_dict = {}
sorted_keys = sorted(distances, key=distances.get)

for w in sorted_keys:
    sorted_dict[w] = distances[w]
