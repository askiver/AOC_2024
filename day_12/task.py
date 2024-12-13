from pathlib import Path
import numpy as np

data = Path("input.txt").read_text()

garden = [[plot for plot in row] for row in data.splitlines()]

max_y, max_x = len(garden), len(garden[0])
directions = [(0,-1), (-1,0), (0,1), (1,0)]

def find_neighbours(pos_y, pos_x, plot, found_neighbours):
    num_neighbours = 0

    for direction in directions:
        dy, dx = direction[0], direction[1]
        new_y, new_x = pos_y + dy, pos_x + dx
        if 0 <= new_y < max_y and 0 <= new_x < max_x:
            if (new_y, new_x) not in found_neighbours and garden[new_y][new_x] == plot:
                found_neighbours.append((new_y, new_x))
                num_neighbours += find_neighbours(new_y, new_x, plot, found_neighbours)
                num_neighbours += 1
    return num_neighbours


def find_perimeter(neighbours):
    perimeter_array = np.zeros((max_y, max_x, 4))
    for neighbour in neighbours:
        y,x = neighbour
        for direction in directions:
            dy,dx = direction[0], direction[1]
            if not (y+dy, x+dx) in neighbours:
                perimeter_array[y,x,directions.index(direction)] = 1

    return np.sum(perimeter_array), perimeter_array

def trace_edge(pos_y, pos_x, direction, perimeter_array):
    next_dir_index = (direction + 1) % 4
    previous_dir_index = (direction-1) % 4
    if perimeter_array[pos_y, pos_x, next_dir_index]:
        return pos_y, pos_x, next_dir_index, 1
    else:
        dy, dx = directions[next_dir_index]
        new_y, new_x = pos_y + dy, pos_x + dx
        if perimeter_array[new_y, new_x, direction]:
            return new_y, new_x, direction, 0
        else:
            dy, dx = directions[direction]
            new_y, new_x = new_y + dy, new_x + dx
            return new_y, new_x, previous_dir_index, 1

def find_num_sides(perimeter_array):
    total_sides = 0
    while np.sum(perimeter_array) > 0:
        indices = np.where(perimeter_array[:, :, 0] > 0)
        org_y, org_x = indices[0][0], indices[1][0]
        org_dir = 0
        y,x,curr_dir, new_sides = trace_edge(org_y, org_x, 0, perimeter_array)
        perimeter_array[y,x,curr_dir] = 0
        total_sides += new_sides
        while (y,x,curr_dir) != (org_y, org_x, org_dir):
            y,x,curr_dir, new_sides = trace_edge(y,x,curr_dir, perimeter_array)
            perimeter_array[y, x, curr_dir] = 0
            total_sides += new_sides

    return total_sides


def find_price(pos_y, pos_x):
    plot = garden[pos_y][pos_x]
    neighbours = []
    area = find_neighbours(pos_y, pos_x, plot, neighbours)
    area = area if area > 0 else 1
    neighbours = neighbours if len(neighbours) > 0 else [(pos_y, pos_x)]
    perimeter, perimeter_neighbours = find_perimeter(neighbours)
    num_sides = find_num_sides(perimeter_neighbours)
    return area * perimeter, neighbours, area * num_sides


visited_plots = []
price = 0
bulk_price = 0
for y in range(max_y):
    for x in range(max_x):
        if (y,x) not in visited_plots:
            local_price, neighbours, local_bulk_price = find_price(y,x)
            price += local_price
            bulk_price += local_bulk_price
            visited_plots.extend(neighbours)

print(price)
print(bulk_price)
