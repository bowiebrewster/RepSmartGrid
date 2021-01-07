import csv

with open(r"C:\Users\bowie\OneDrive\Desktop\programmeren\district-1_batteries.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    #Array of batteries 
    MatrixBatt = []

    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            
            line_count += 1

            Cor = row[0]
            Cap = row[1]

            [CorX,CorY]= Cor.split(",")

            CorX=int(CorX)
            CorY=int(CorY)

            Cap = int(Cap[0:-2])
            
            MatrixBatt.append([CorX,CorY,Cap])

    print(f'Processed {line_count} lines.')

with open(r"C:\Users\bowie\OneDrive\Desktop\programmeren\district-1_houses.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    # Array of houses
    MatrixHouses = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            
            line_count += 1

            XCor = int(row[0])
            YCor = int(row[1])
            MaxOut = float(row[2])

            MatrixHouses.append([XCor,YCor,MaxOut])


    print(f'Processed {line_count} lines.')


Array3d=[]

for i in range(len(MatrixHouses)):
    HouseList = MatrixHouses[i]
    HouseX = HouseList[0]
    HouseY = HouseList[1]
    
    deltalist = []

    for BatList in MatrixBatt:
        BatX = BatList[0]
        BatY = BatList[1]

        DeltaX = abs(BatX-HouseX)
        DeltaY = abs(BatY-HouseY)

        deltalist.append([DeltaX,DeltaY])

    Array3d.append(deltalist)

print("difference array:")
# Row is house number
# Column is battery number 
# Entry is [deltax,deltay]


for r in Array3d:
    for c in r:
        print(c,end = " ")
    print()






