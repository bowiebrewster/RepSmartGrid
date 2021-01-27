import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from code.algorithms import simulatedannealing as sa
from code.algorithms import random as r
from code.classes.district import District

district = District(2)
algorithm = r.Random(district)
algorithm.run(False, False)
calib = sa.SimulatedAnnealing(algorithm)

xx = np.linspace(0.01, 0.05, num=100) # cooling rate
yy = np.linspace(20, 40, num=100) # temperature
X, Y = np.meshgrid(xx, yy)
Z = []
for Xrow, Yrow in zip(X, Y):
    z = []
    for cr, start_temp in zip(Xrow, Yrow):
        print(f"cooling rate {cr} and start temp {start_temp}")
        cost = calib.calibrate(cr, start_temp)
        z.append(cost)
    Z.append(z)
    if len(Z) % 10 == 0:
        print(f'Hoppakee, 10% erbij bro')

Z = np.array(Z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0)
loc = np.argwhere(Z == np.min(Z)[0])
i, j = loc[0], loc[1]
best_cr = xx[i]
best_T = yy[j]
print(f"Best cooling rate: {best_cr} and Best temperature: {best_T}")
print(f"{Z[i][j]}")
plt.show()
