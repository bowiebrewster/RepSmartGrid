import time

from code.classes.district import District

from code.algorithms import greedy, random, simulatedannealing

from code.visualisation import visualise

if __name__ == "__main__":
    number = int(input("What district would you like to optimize? "))
    # start = time.time()
    district = District(number)
    r = random.Random(district)
    r.run()
    print("Starting Simulated Annealing")
    sa = simulatedannealing.SimulatedAnnealing(r, 30, 100)
    sa.run()
    # print(f"{time.time() - start}")
