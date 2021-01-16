import matplotlib.pyplot as plt
import random
import copy
import numpy as np
import operator
import itertools
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

# all_costs = [74032, 75670, 75292, 73709, 77650, 74788, 75112, 75562, 75616, 77218, 76534, 76246, 76066, 80764, 76570]
# # print(all_costs)
# x = [i for i in range(1, len(all_costs) + 1)]
# fig = plt.figure()

# plt.bar(x, all_costs, color ='maroon', width = 0.9) 
  
# plt.xlabel("Verschillende allocaties") 
# plt.ylabel("Kosten") 
# plt.title("Kostenverdeling random allocaties") 
# plt.show() 

x = ['1', '2', '3']
y = ['4', '5', '6']
my_dict = {'henk': x, 'anita': y}
rand_b1 = random.choice(list(my_dict.keys()))
print(rand_b1)
rand_h1 = random.choice(my_dict[rand_b1])
print(rand_h1)