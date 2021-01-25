import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import random
# import copy
import numpy as np
# import operator
# import itertools
# import collections
import math

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

# x = ['1', '2', '3']
# y = ['4', '5', '6']
# my_dict = {'henk': x, 'anita': y}
# rand_b1 = random.choice(list(my_dict.keys()))
# print(rand_b1)
# rand_h1 = random.choice(my_dict[rand_b1])
# print(rand_h1)

# class Node:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.sum = x + y
#         self.product = x * y

#     def __str__(self):
#         return f'{self.x}, {self.y}, {self.sum}, {self.product}'

# piet = Node(4,5)
# henk = Node(6, 4)
# del henk.product, henk.sum
# print(piet)

# ledger = [('hoi', 'henk', 21), ('hi', 'anita', 15), ('ghello', 'bob', 35), ('hey', 'roens', 14)]
# smallest = min(ledger, key=lambda x: x[2])
# print(smallest)

# my_dict = {'henk': 1, 'anita': 2, 'bob': 3, 'herman': 4, 'ingrid': 5, 'sjonnie': 6}
# batteries = {'b1': [1, 4, 6,7, 8,9], 'b2': [2, 3, 5, 10], 'b3': [11, 12, 13, 14, 15]}
# print(batteries)
# print("-------")
# random_batteries = random.sample(list(batteries.items()), 2)
# batt1, houses1 = random_batteries[0]
# batt2, houses2 = random_batteries[1]
# random_house1 = random.choice(houses1)
# random_house2 = random.choice(houses2)
# batteries[batt1].remove(random_house1)
# print(batteries)

# r = random.random()
# print(r)
# print(r)

def f(x):
    return math.cos(x) + math.sin(x) + 10 * math.sin(0.1 * x)

def acceptance_probability(s_old, s_new, temp):
    if s_new < s_old:
        return 1.0
    else:
        return math.exp((s_old - s_new) / temp)

def main(cr, start_temp, k_max=300):
    # start_temp = 30
    # k_max = 300
    # alpha = 0.01
    current_E = f(random.uniform(0, 50))
    current_temp = start_temp
    i = 0
    while current_temp > 0.01:
        current_temp = start_temp * (1 - cr)**i # current_temp -= cr
        for k in range(k_max):
            new_E = f(random.uniform(0, 50))
            if acceptance_probability(current_E, new_E, current_temp) >= random.random():
                current_E = new_E
        i += 1

    return current_E

if __name__ == '__main__':
    # x represents cooling rate
    # y represents temperature
    # print(main(0.001, 20))
    xx = np.linspace(0.001, 0.1, num=100)
    yy = np.linspace(20, 40, num=100)
    X, Y = np.meshgrid(xx, yy)
    Z = []
    for Xrow, Yrow in zip(X, Y):
        z = []
        for cr, start_temp in zip(Xrow, Yrow):
            z.append(main(cr, start_temp))
        Z.append(z)
        if len(Z) % 10 == 0:
            print(f'Hoppakee, 10% erbij bro')
  
    Z = np.array(Z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
    
    plt.show()
    m = np.amin(Z)
    print(m)

    # for i in range(1000):
    #     if i % 100 == 0:
    #         print(f"{i/10}%")

    #     a.append(main())
    # print(min(a))
    