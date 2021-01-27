from time import time
import os

from code.classes.district import District
from code.algorithms import greedy, random, simulatedannealing, hillclimber
from code.visualisation import visualise


if __name__ == "__main__":

    print("In a district we are trying to optimally connect houses with solar panels to batteries to save energy.")
    print("It is up to you to help us with this optimization problem!\n")

    number = int(input("What district would you like to optimize? "))
    while number != 1 and number != 2 and number != 3:
        number = int(input("What district would you like to optimize? "))

    algo1 = input("What algorithm would you like to apply? Type 'r' for random and 'g' for greedy. ")
    while algo1.lower()[0] != 'r' and algo1.lower()[0] != 'g' and algo1 == '':
        algo1 = input("What algorithm would you like to apply? Type 'r' for random and 'g' for greedy. ")
    
    if 'g' in algo1:
        print("In greedy version 1 we put the batteries in a certain order and connect them one for one with the closest houses.")
        print("In greedy version 2 we sort the houses based on their output and then we connect each house with the closest battery.")
        version = int(input("Would you like to run version 1 or 2 of greedy? Type 1 for version 1 and 2 for version 2. "))
        while version != 1 and version != 2 and version == '':
            version = int(input("What version of greedy would you like to implement? "))
    else:
        version = None

    shared = input("Do you want to share lines? Type y(es) or n(o). ")
    while shared.lower()[0] != 'y' and shared.lower()[0] != 'n' and shared == '':
        shared = input("Do you want to share lines? Type y(es) or n(o). ")

    save = input("Do you want to save the figure? Type y(es) or n(o). ")
    while save.lower()[0] != 'y' and save.lower()[0] != 'n' and save == '':
        save = input("Do you want to save the figure? Type y(es) or n(o). ")
    
    print()

    district = District(number)
    if 'r' in algo1:
        algo = random.Random(district)
    else:
        algo = greedy.Greedy(district)

    if 'y' in shared:
        shared1 = True
    else:
        shared1 = False

    if 'y' in save:
        save1 = True
    else:
        save1 = False

    start1 = time()

    if version is not None:
        if version == 1:
            algo.run_v1(shared1, save1)
        else:
            algo.run_v2(shared1, save1)
    else:
        algo.run(shared1, save1)

    end1 = time()

    print()

    if algo.feasible:
        print(f"The algorithm found a solution in {round(end1 - start1, 2)} seconds.\n")
    else:
        print(f"The algorithm has found no feasible solution.\n")
        exit()

    better = input("Would you like to improve this result? Type y(es) or n(o). ")
    while better.lower()[0] != 'y' and better.lower()[0] != 'n' and better == '':
        better = input("Would you like to improve previous result? Type y(es) or n(o). ")
    
    if better.lower()[0] == 'n':
        exit()

    if 'y' in better.lower():
        algo2 = input("What second algorithm would you like to apply? Type 'hc' for hill climber and 'sa' for simulated annealing. ")
        while algo2.lower()[0] != 'h' and algo2.lower()[0] != 's' and algo2 == '':
            algo2 = input("What second algorithm would you like to apply? Type 'hc' for hill climber and 'sa' for simulated annealing. ")

    shared = input("Do you want to share lines in the second algorithm? Type y(es) or n(o). ")
    while shared.lower()[0] != 'y' and shared.lower()[0] != 'n' and shared == '':
        shared = input("Do you want to share lines? Type y(es) or n(o). ")

    save = input("Do you want to save the figure of the second algorithm's allocation? Type y(es) or n(o). ")
    while save.lower()[0] != 'y' and save.lower()[0] != 'n' and save == '':
        save = input("Do you want to save the figure? Type y(es) or n(o). ")

    print()
    
    if 'y' in shared:
        shared2 = True
    else:
        shared2 = False

    if 'y' in save:
        save2 = True
    else:
        save2 = False

    start2 = time()

    if algo2 == 'hc':
        hc = hillclimber.HillClimber(algo)
        if version is not None:
            hc.run(shared2, save2, version)
        else:
            hc.run(shared2, save2, None)
    else:
        sa = simulatedannealing.SimulatedAnnealing(algo)
        if version is not None:
            sa.run(0.005, 25.5, shared2, save2, version)
        else:
            sa.run(0.005, 25.5, shared2, save2, None)

    end2 = time()

    print(f"\nThe second algorithm found a solution in {round(end2 - start2, 2)} seconds.")