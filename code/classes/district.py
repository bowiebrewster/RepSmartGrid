from .battery import Battery
from .house import House

class District():

    def __init__(self, number):
        self.number = number
        self.path = f'data/district_{number}/district-{number}_'
        self.batteries = []
        self.houses = []
        self.load_files()

    def load_files(self):
        files = [self.path + 'batteries.csv', self.path + 'houses.csv']
        for filename in files:
            with open(filename, 'r') as file:
                data = file.readlines()[1:]
                for i, row in enumerate(data):
                    row = row.replace('"', '').split(',')
                    x, y, OC = int(row[0]), int(row[1]), float(row[2].rstrip())
                    if len(data) == 5:
                        self.batteries.append(Battery(i + 1, x, y, OC))
                    else:
                        self.houses.append(House(i + 1, x, y, OC))