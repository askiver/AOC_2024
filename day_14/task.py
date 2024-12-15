import copy
from pathlib import Path
import re
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=np.inf)

file_path = Path("input.txt")
pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
robot_dict = {}
height, width = 103, 101
robot_array = np.zeros((height, width))
for idx, line in enumerate(file_path.read_text().splitlines()):
    if match := pattern.search(line):
        px, py, vx, vy = match.groups()
        robot_dict[idx] = (int(py),int(px)), (int(vy),int(vx))
        robot_array[int(py),int(px)] += 1
num_robots = len(robot_dict)

directions = [(0,-1), (-1,0), (0,1), (1,0)]
def find_neighbours(pos_y, pos_x, found_neighbours):
    num_neighbours = 0

    for direction in directions:
        dy, dx = direction[0], direction[1]
        new_y, new_x = pos_y + dy, pos_x + dx
        if 0 <= new_y < height and 0 <= new_x < width:
            if (new_y, new_x) not in found_neighbours and robot_array[new_y][new_x]:
                found_neighbours.append((new_y, new_x))
                num_neighbours = find_neighbours(new_y, new_x, found_neighbours) + 1
    return num_neighbours


half_height = height // 2
half_width = width // 2
num_neighbours = 0
best_image = None

for i in tqdm(range(10000)):
    for robot_idx in range(num_robots):
        pos, velocity = robot_dict[robot_idx]
        py, px = pos
        robot_array[py, px] -= 1
        vy, vx = velocity
        py = (py + vy) % height
        px = (px + vx) % width
        robot_dict[robot_idx] = ((py, px), velocity)
        robot_array[py, px] += 1

    if i == 99:
        safety_factor = 1
        safety_factor *= np.sum(robot_array[:half_height, :half_width])
        safety_factor *= np.sum(robot_array[:half_height, half_width + 1:])
        safety_factor *= np.sum(robot_array[half_height + 1:, :half_width])
        safety_factor *= np.sum(robot_array[half_height + 1:, half_width + 1:])
        print(int(safety_factor))

    visited_places = []
    relevant_indices = np.where(robot_array > 0)

    for y, x in zip(*relevant_indices):
        if (y,x) not in visited_places:
            neighbour_list = []
            neighbours = find_neighbours(y,x,neighbour_list)
            if neighbours > num_neighbours:
                num_neighbours = neighbours
                tree_index = i+1
                best_image = copy.deepcopy(robot_array)
            visited_places.extend(neighbour_list)


print(tree_index)
plt.imshow(best_image, cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.show()