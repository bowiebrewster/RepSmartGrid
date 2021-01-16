from code.classes.district import *

from code.algorithms import greedy, random

from code.visualisation import visualise

if __name__ == "__main__":
    number = int(input("What district would you like to optimize? "))
    district = District(f'data/district_{number}/district-{number}_')
    r = random.Random(district)
    r.run()
    visualise.show(r)