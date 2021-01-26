import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import random
import copy
import numpy as np
import operator
import itertools
import collections
import math

    xx = np.linspace(0.01, 0.05, num=100) # cooling rate
    yy = np.linspace(20, 40, num=100) # Temperature
    X, Y = np.meshgrid(xx, yy)
    Z = []
    for Xrow, Yrow in zip(X, Y):
        z = []
        for cr, start_temp in zip(Xrow, Yrow):
            z.append(sa.calibrate(cr, start_temp))
        Z.append(z)
        if len(Z) % 10 == 0:
            print(f'Hoppakee, 10% erbij bro')
  
    Z = np.array(Z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0)
    i, j  = np.unravel_index(Z.argmin(), Z.shape())
    print(f'Best i = {i} - Best j = {j}')
    print(Z[i][j])
    print(f'{time.time() - start}')
    plt.show()
