import time
import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm 

from code.classes.district import District

from code.algorithms import greedy, random, simulatedannealing, hillclimber

from code.visualisation import visualise

if __name__ == "__main__":
    number = int(input("What district would you like to optimize? "))
    while number != 1 and number != 2 and number != 3:
        number = int(input("What district would you like to optimize? "))

    algo1 = input("What algorithm would you like to apply? Type 'r' for random and 'g' for greedy. ")
    while 'r' not in algo1.lower() and 'g' not in algo1.lower():
        algo1 = input("What algorithm would you like to apply? Type 'r' for random and 'g' for greedy. ")
    
    if 'g' in algo1:
        print("In greedy version 1 we put the batteries in a certain order and connect them one for one with the closest houses.")
        print("In greedy version 2 we sort the houses based on their output and then we connect each house with the closest battery.")
        version = int(input("Would you like to run version 1 or version 2 of greedy? Type 1 for version 1 and 2 for version 2. "))
        while version != 1 and version != 2:
            version = int(input("What version of greedy would you like to implement? "))

    shared = input("Do you want to share lines? Type y(es) or n(o). ")
    while 'y' not in mst.lower() and 'n' not in mst.lower():
        shared = input("Do you want to share lines? Type y(es) or n(o). ")

    save = input("Do you want to save the figure? Type y(es) or n(o). ")
    while 'y' not in save.lower() and 'n' not in save.lower():
        save = input("Do you want to save the figure? Type y(es) or n(o). ")

    start = time.time()
    district = District(number)
    if 'r' in algo1:
        algo = random.Random(district)
    elif 'g' in algo1:
        algo = greedy.Greedy(district)

    if 'y' in mst:
        mst = True
    elif 'n' in mst:
        mst = False

    if 'y' in save:
        save = True
    elif 'n' in save:
        save = False

    try:
        print("hoi")
        if version == 1:
            print("hallo")
            algo.run_v1(mst, save)
        elif version == 2:
            algo.run_v2(mst, save)
    except:
        algo.run(mst, save)

    better = input("Would you like to improve this result? Type y(es) or n(o). ")
    while 'y' not in better.lower() and 'n' not in better.lower():
        better = input("Would you like to improve previous result? Type y(es) or n(o). ")

    if 'y' in better.lower():
        algo2 = input("What second algorithm would you like to apply? Type 'hc' for hill climber and 'sa' for simulated annealing. ")
        while 'hc' not in algo2.lower() and 'sa' not in algo2.lower():
            algo2 = input("What second algorithm would you like to apply? Type 'hc' for hill climber and 'sa' for simulated annealing. ")

    if 'y' in better:
        if 'hc' in algo2:
            hc = hillclimber.HillClimber(algo)
            if shared:
                hc.run_shared(shared, save)
            else:
                hc.run_unique(shared, save)
        elif 'sa' in algo2:
            sa = simulatedannealing.SimulatedAnnealing(algo)
            if shared:
                sa.run_shared(0.01, 25, shared, save)
            else:
                sa.run_unique(0.01, 25, shared, save)

    # 29950
    # 29977
    # 30607
    # 32533

    # xx = np.linspace(0.5, 1, num=10) # cooling rate
    # yy = np.linspace(20, 40, num=3) # Temperature
    # X, Y = np.meshgrid(xx, yy)
    # Z = []
    # for Xrow, Yrow in zip(X, Y):
    #     z = []
    #     for cr, start_temp in zip(Xrow, Yrow):
    #         z.append(sa.calibrate(cr, start_temp))
    #     Z.append(z)
    #     if len(Z) % 3 == 0:
    #         print(f'Hoppakee, 10% erbij bro')
  
    # Z = np.array(Z)
    
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
    #                    linewidth=0)
    # i, j  = np.unravel_index(Z.argmin(), Z.shape())
    # print(f'Best i = {i} - Best j = {j}')
    # print(Z[i][j])
    # print(f'{time.time() - start}')
    # plt.show()
