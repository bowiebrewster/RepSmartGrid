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
    # visualise.show_r(r)
    # g = greedy.Greedy(district)
    # g.run_v1()
    print("Starting Simulated Annealing")
    sa = simulatedannealing.SimulatedAnnealing(r, 20, 100)
    sa.run()
    # visualise.show_sa(sa)
    # print(f"{time.time() - start}")
