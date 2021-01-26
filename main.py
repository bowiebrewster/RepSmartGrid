import time
import numpy as np 
import matplotlib.pyplot as plt 
import os

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm 

from code.classes.district import District
from code.algorithms import greedy, random, simulatedannealing, hillclimber
from code.visualisation import visualise

if __name__ == "__main__":
    number = input("What district would you like to optimize? ")
    while number != 1 and number != 2 and number != 3 and number == '':
        number = input("What district would you like to optimize? ")
    number = int(number)

    algo1 = input("What algorithm would you like to apply? Type 'r' for random and 'g' for greedy. ")
    while algo1.lower()[0] != 'r' and algo1.lower()[0] != 'g' and algo1 == '':
        algo1 = input("What algorithm would you like to apply? Type 'r' for random and 'g' for greedy. ")
    
    if 'g' in algo1:
        print("In greedy version 1 we put the batteries in a certain order and connect them one for one with the closest houses.")
        print("In greedy version 2 we sort the houses based on their output and then we connect each house with the closest battery.")
        version = input("Would you like to run version 1 or 2 of greedy? Type 1 for version 1 and 2 for version 2. ")
        while version != 1 and version != 2 and version == '':
            version = input("What version of greedy would you like to implement? ")
        version = int(version)

    shared1 = input("Do you want to share lines? Type y(es) or n(o). ")
    while shared1.lower()[0] != 'y' and shared1.lower()[0] != 'n' and shared1 == '':
        shared1 = input("Do you want to share lines? Type y(es) or n(o). ")

    save1 = input("Do you want to save the figure? Type y(es) or n(o). ")
    while save1.lower()[0] != 'y' and save1.lower()[0] != 'n' and save1 == '':
        save1 = input("Do you want to save the figure? Type y(es) or n(o). ")
    
    print()

    district = District(number)
    if 'r' in algo1:
        algo = random.Random(district)
    elif 'g' in algo1:
        algo = greedy.Greedy(district)

    if 'y' in shared1:
        shared1 = True
    elif 'n' in shared1:
        shared1 = False

    if 'y' in save1:
        save1 = True
    elif 'n' in save1:
        save1 = False

    start1 = time.time()
    try:
        if version == 1:
            algo.run_v1(shared1, save1)
        elif version == 2:
            algo.run_v2(shared1, save1)
    except:
        algo.run(shared1, save1)
    end1 = time.time()
    if algo.feasible:
        print()
        print(f"The algorithm found a solution in {end1 - start1} seconds.")
    else:
        print(f"The algorithm has found no feasible solution.")
        exit()
    print()

    better = input("Would you like to improve this result? Type y(es) or n(o). ")
    while better.lower()[0] != 'y' and better.lower()[0] != 'n' and better == '':
        better = input("Would you like to improve previous result? Type y(es) or n(o). ")
    
    if better.lower()[0] == 'n':
        exit()

    if 'y' in better.lower():
        algo2 = input("What second algorithm would you like to apply? Type 'hc' for hill climber and 'sa' for simulated annealing. ")
        while algo2.lower()[0] != 'h' and algo2.lower()[0] != 's' and algo2 == '':
            algo2 = input("What second algorithm would you like to apply? Type 'hc' for hill climber and 'sa' for simulated annealing. ")

    shared2 = input("Do you want to share lines in the second algorithm? Type y(es) or n(o). ")
    while shared2.lower()[0] != 'y' and shared2.lower()[0] != 'n' and shared2 == '':
        shared2 = input("Do you want to share lines? Type y(es) or n(o). ")

    save2 = input("Do you want to save the figure of the second algorithm's allocation? Type y(es) or n(o). ")
    while save2.lower()[0] != 'y' and save2.lower()[0] != 'n' and save2 == '':
        save2 = input("Do you want to save the figure? Type y(es) or n(o). ")

    if 'y' in shared2:
        shared2 = True
    elif 'n' in shared2:
        shared2 = False

    if 'y' in save2:
        save2 = True
    elif 'n' in save2:
        save2 = False

    start2 = time.time()
    if algo2 == 'hc':
        hc = hillclimber.HillClimber(algo)
        try:
            if version:
                hc.run_unique(shared2, save2, version)
        except:
            hc.run_unique(shared2, save2, None)
    elif algo2 == 'sa':
        sa = simulatedannealing.SimulatedAnnealing(algo)
        try:
            if version:
                sa.run_unique(0.01, 25, shared2, save2, version)
        except:
            sa.run_unique(0.01, 25, shared2, save2, None)
    end2 = time.time()
    print()
    print(f"The second algorithm found a solution in {end2 - start2} seconds.")