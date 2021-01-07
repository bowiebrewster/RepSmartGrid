import csv
import random
path = f'data/district_1/district-1_'
files = [path + 'batteries.csv', path + 'houses.csv'] # de twee bestanden opslaan in lijst
for filename in files:
    with open(filename, 'r') as file:
        data = file.readlines()[1:]
        for row in data:
            row = row.replace('"', '').split(',')
            x, y, OC = int(row[0]), int(row[1]), float(row[2].rstrip())
            if len(data) == 5:
                self.batteries.append(Battery(x, y, OC))
            else:
                self.houses.append(House(x, y, OC))