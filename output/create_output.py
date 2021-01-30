import json

def create_output(name, number, costs, connections, shared, mst):
    output = []
    general_data = {}


    general_data['district'] = number
    if shared:
        general_data['costs-shared'] = costs
    else:
        general_data['costs-unique'] = costs

    output.append(general_data)

    if shared:
        all_paths = get_shared_paths(mst)
    else:
        all_paths = get_unique_paths(connections)

    for battery, houses in connections.items():    
        battery_data = {}

        battery_data['location'] = f"{battery.x},{battery.y}"
        battery_data['capacity'] = battery.capacity
        battery_data['houses'] = []
        complete_paths = all_paths[battery]
        for house in houses:
            house_data = {}
            house_data['location'] = f"{house.x},{house.y}"
            house_data['output'] = house.output
            paths = complete_paths[(house.x, house.y)]
            house_data['cables'] = paths
            battery_data['houses'].append(house_data)
        output.append(battery_data)
    with open(f"output/{name.lower()}/district {number} output {costs}.txt", 'w') as f:
        f.write(json.dumps(output, indent=5))
   
def get_shared_paths(mst):
    all_paths = {}
    for battery, paths in mst.items():
        all_paths[battery] = {}
        coordinates = []
        for xx, yy in paths:
            subcor = []
            for x, y in zip(xx, yy):
                subcor.append((x,y))
            coordinates.append(subcor)
        for i in range(1, len(coordinates)+1):
            complete_house_path = []
            house_branch = coordinates[-i]
            house_cor = house_branch[0]
            begin = house_branch[-1]
            for pair in house_branch:
                complete_house_path.append(f"{pair[0]},{pair[1]}")
  
            sub_coordinates = coordinates[:-i]
            sub_coordinates.reverse()
            for coors in sub_coordinates:
                if begin in coors:
                    idx = coors.index(begin)
                    if idx == len(coors) -1:
                        continue
                    house_branch = coors[(idx+1):]
                    for pair in house_branch:
                        complete_house_path.append(f"{pair[0]},{pair[1]}")
                begin = house_branch[-1]
            all_paths[battery][house_cor] = complete_house_path

    return all_paths

def get_unique_paths(connections):
    all_paths = {}

    for battery, houses in connections.items():
        all_paths[battery] = {}
        batt_cor = (battery.x, battery.y)
        # print(f"the battery x: {battery.x} and y: {battery.y}")
        for house in houses:
            x = []
            y = []
            # print(f"the house x: {house.x} and y: {house.y}")

            if house.y != battery.y:
                ysteps = abs(house.y - battery.y) + 1
                for j in range(ysteps):
                    # print(f"y coordinate of the house is now {house.y}")
                    y.append(house.y)
                    if house.y < battery.y:
                        house.y += 1
                    else:
                        house.y -= 1
            
            if house.x != battery.x:
                xsteps = abs(house.x - battery.x) + 1
                for i in range(xsteps):
                    # print(f"x coordinate of house is now {house.x}")
                    x.append(house.x)
                    if house.x < battery.x:
                        house.x += 1
                    else:
                        house.x -= 1
            
            if house.x == battery.x:
                for k in range(len(y) + 1):
                    x.append(house.x)
            
            if house.y == battery.y:
                for n in range(len(x) + 1):
                    y.append(house.y)
            # print(f"the length of x is now {len(x)}")
            # print(x)
            # print(f"the length of y is now {len(y)}")
            # print(y)
            # print("___________")
 
            if len(x) < len(y):
                while len(x) != len(y):
                    last = x[-1]
                    x.append(last)
            elif len(x) > len(y):
                while len(x) != len(y):
                    first = y[0]
                    y.insert(0, first)
            # print(f"the length of x is now {len(x)}")
            # print(x)
            # print(f"the length of y is now {len(y)}")
            # print(y)

            complete_house_path = []
            for xx, yy in zip(x, y):
                complete_house_path.append(f"{xx},{yy}")
            # print(complete_house_path)
            all_paths[battery][(house.x, house.y)] = complete_house_path

    return all_paths