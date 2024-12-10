from tqdm import tqdm
import numpy as np
map = []
for line in open("input.txt", 'r'):
    map.append([sign for sign in line.strip()])

# Task 1
max_y, max_x = len(map)-1, len(map[0])-1
dir_dict = {
    (-1,0): np.array([0,1], dtype=int),
    (0,1): np.array([1,0], dtype=int),
    (1,0): np.array([0,-1], dtype=int),
    (0,-1): np.array([-1,0], dtype=int)
}

pos_array = np.zeros((max_y+1, max_x+1))
# Find initial position
org_pos = next((y,x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == '^')
pos = np.array(org_pos, dtype=int)
current_dir = np.array([-1,0], dtype=int)
while True:
    y,x = pos
    if y > max_y or x > max_x or np.any(pos < 0):
        break
    elif map[y][x] == '#':
        pos = pos - current_dir
        current_dir = dir_dict[*current_dir]
    else:
        pos_array[y][x] = 1
        pos = pos + current_dir


print(int(np.sum(pos_array)))
traversed_path = np.where(pos_array == 1)


# Task 2

pos_array = np.zeros((max_y+1, max_x+1, 4))
current_dir = np.array([-1,0])
total_loops = 0

key_dict = {
    (-1,0): 0,
    (0,1): 1,
    (1,0): 2,
    (0,-1): 3,
}

def check_bounds(pos, dir):
    y,x = pos + dir
    if y > max_y or x > max_x or np.any(pos < 0):
        return False
    return True

def step(pos, dir):
    next_pos = pos + dir
    y,x = next_pos
    if map[y][x] == "#":
        next_dir = dir_dict[*dir]
        return pos, next_dir
    return next_pos, dir

def check_loop():
    pos = np.array(org_pos)
    pos_array = np.zeros((max_y+1, max_x+1, 4))
    current_dir = np.array([-1,0])
    while check_bounds(pos, current_dir):
        y, x = pos
        next_pos, next_dir = step(pos, current_dir)
        dict_key = key_dict[*next_dir]
        if pos_array[y,x,dict_key] == 1:
            return True
        else:
            if not np.array_equal(next_pos, pos):
                pos_array[y,x,dict_key] = 1
                pos = next_pos
            current_dir = next_dir
    return False

for index in tqdm(list(zip(traversed_path[0], traversed_path[1]))):
    y,x = index
    if map[y][x] == "^":
        continue
    map[y][x] = "#"
    total_loops += check_loop()
    map[y][x] = "."

print(total_loops)
