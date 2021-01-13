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

afstanden = {
    "Battery 1": {
        "House 1": 39,
        "House 2": 24,
        "House 3": 43,
        "House 4": 45,
        "House 5": 50,
        "House 6": 22,
        "House 7": 27,
        "House 8": 36,
        "House 9": 54,
        "House 10": 48
    },

    "Battery 2": {
        "House 1": 43,
        "House 2": 28,
        "House 3": 37,
        "House 4": 49,
        "House 5": 54,
        "House 6": 28,
        "House 7": 33,
        "House 8": 42,
        "House 9": 58,
        "House 10": 52
    },

    "Battery 3": {
        "House 1": 52,
        "House 2": 37,
        "House 3": 48,
        "House 4": 58,
        "House 5": 63,
        "House 6": 33,
        "House 7": 24,
        "House 8": 37,
        "House 9": 67,
        "House 10": 61
    },

    "Battery 4": {
        "House 1": 39,
        "House 2": 26,
        "House 3": 21,
        "House 4": 45,
        "House 5": 50,
        "House 6": 44,
        "House 7": 49,
        "House 8": 58,
        "House 9": 54,
        "House 10": 48
    },

    "Battery 5": {
        "House 1": 33,
        "House 2": 44,
        "House 3": 47,
        "House 4": 23,
        "House 5": 20,
        "House 6": 48,
        "House 7": 57,
        "House 8": 44,
        "House 9": 14,
        "House 10": 20
    }
}

for batterij, huis_met_afstanden in afstanden.items():
    print("We zijn nu bij batterij:")
    print(batterij)
    print("En hierbij hoort deze dictionary met als keys de huizen en als values de afstanden van de huizen tot de batterij:")
    print(afstanden[batterij])
    for huis, manhattan_distance in huis_met_afstanden.items():
        print("En dit is de manhattan distance van een huis in deze dictionary tot de batterij:")
        print(huis_met_afstanden[huis])
    print("-------------------")
    print("einde van deze batterij, door naar de volgende iteratie")
    print("-------------------")