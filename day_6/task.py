import numpy as np
map = []
for line in open("input.txt", 'r'):
    map.append([sign for sign in line.strip()])

map = np.array(map)

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
pos = next((y,x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == '^')
pos = np.array(pos, dtype=int)
current_dir = np.array([-1,0], dtype=int)
while True:
    if pos[0] > max_y or pos[1] > max_x or np.any(pos < 0):
        break
    elif map[tuple(pos)] == '#':
        pos = pos - current_dir
        current_dir = dir_dict[tuple(current_dir)]
    else:
        pos_array[tuple(pos)] = 1
        pos = pos + current_dir


print(int(np.sum(pos_array)))


# Task 2

pos_array = np.zeros((max_y+1, max_x+1, 4))
org_pos = next((y,x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == '^')
org_pos = np.array(org_pos)
current_dir = np.array([-1,0])
total_loops = 0

key_dict = {
    (-1,0): 0,
    (0,1): 1,
    (1,0): 2,
    (0,-1): 3,
}

def check_loop(pos, dir, map_copy):
    copy_pos_array = pos_array.copy()
    current_pos, current_dir = pos, dir
    while not (current_pos[0] + current_dir[0] > max_y or current_pos[1] + current_dir[1] > max_x or current_pos[0] + current_dir[0] < 0 or current_pos[1] + current_dir[1] < 0):
        next_pos = pos + dir
        dict_key = key_dict[tuple(current_dir)]
        if map_copy[tuple(next_pos)] == '#':
            current_dir = dir_dict[tuple(current_dir)]
        elif copy_pos_array[tuple(current_pos)][dict_key] > 0:
            return True
        else:
            copy_pos_array[tuple(current_pos)][dict_key] = 1
            current_pos += current_dir
    return False

pos = org_pos
while True:
    dict_key = key_dict[tuple(current_dir)]
    next_pos = pos + current_dir
    if next_pos[0] > max_y or next_pos[1] > max_x or np.any(pos < 0):
        break
    elif map[tuple(next_pos)] == '#':
        current_dir = dir_dict[tuple(current_dir)]
    elif np.array_equal(next_pos, org_pos):
        pos_array[tuple(pos)][dict_key] = 1
        pos += current_dir
    else:
        map_copy = map.copy()
        map_copy[tuple(pos+current_dir)] = '#'
        result = check_loop(pos.copy(), dir_dict[tuple(current_dir)], map_copy)
        pos_array[tuple(pos)][dict_key] = 1
        pos += current_dir
        total_loops += result

print(total_loops)
