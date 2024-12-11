from pathlib import Path
from pickletools import uint1
import time
import numpy as np
from collections import defaultdict

start_time = time.perf_counter()
data = Path("input.txt").read_text()

map = [[antenna for antenna in row] for row in data.splitlines()]
map_array = np.array(map)
max_y, max_x = len(map), len(map[0])

antenna_array = np.zeros((max_y, max_x))
antenna_positions = defaultdict(list)
antenna_locations = np.where(map_array != ".")

for y,x in zip(*antenna_locations):
    antenna_type = map[y][x]
    antenna_positions[antenna_type].append((y,x))

# Find antenna positions

for y,x in zip(*antenna_locations):
    antenna_type = map[y][x]
    for position in antenna_positions[antenna_type]:
        if position != (y,x):
            pos_y, pos_x = position
            dy, dx = pos_y-y, pos_x-x
            end_y, end_x = pos_y + dy, pos_x + dx
            if 0 <= end_y < max_y and 0 <= end_x < max_x:
                antenna_array[end_y][end_x] = 1

print(antenna_array.sum())

# Task 2
antenna_array.fill(0)

for y,x in zip(*antenna_locations):
    antenna_type = map[y][x]
    antenna_array[y][x] = 1
    for position in antenna_positions[antenna_type]:
        if position != (y,x):
            pos_y, pos_x = position
            dy, dx = pos_y - y, pos_x - x
            while True:
                pos_y, pos_x = pos_y + dy, pos_x + dx
                if 0 <= pos_y < max_y and 0 <= pos_x < max_x:
                    antenna_array[pos_y][pos_x] = 1
                else:
                    break



print(antenna_array.sum())
print(time.perf_counter() - start_time)