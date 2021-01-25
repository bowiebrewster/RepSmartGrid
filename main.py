from datetime import datetime

from code.classes.district import District
from code.algorithms import *
from code.visualisation import visualise

if __name__ == "__main__":
    number = int(input("What district would you like to optimize? "))
    district = District(number)
    r = random.Random(district)

    # print de begintijd om de runtijd uit te rekenen
    begin_runtime = datetime.now()
    print(f"begin runtime: {begin_runtime}")
    r.run()

    print("Starting Simulated Annealing at {datetime.now()}")
    sa = simulatedannealing.SimulatedAnnealing(r, 20, 10)
    sa.run()
    end_runtime = datetime.now()
    print(f"end runtime: {end_runtime}")

    # print de runtijd
    total_runtime = end_runtime - begin_runtime    
    print(f"total runtime: {total_runtime}")