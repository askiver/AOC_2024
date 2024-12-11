from multiprocessing import Pool
import numpy as np
import time
sign_dict = {"#":1, ".":0, "^":-1}
start_time = time.perf_counter()
map = []
for line in open("input.txt", 'r'):
    map.append([sign_dict[sign] for sign in line.strip()])

map = np.array(map)

# Task 1
max_y, max_x = len(map)-1, len(map[0])-1
dir_dict = {
    (-1,0): np.array([0,1], dtype=int),
    (0,1): np.array([1,0], dtype=int),
    (1,0): np.array([0,-1], dtype=int),
    (0,-1): np.array([-1,0], dtype=int)
}
guard_path = []
pos_array = np.zeros((max_y+1, max_x+1))
# Find initial position
org_pos = next((y,x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == -1)
map[*org_pos] = 0
pos = np.array(org_pos, dtype=int)
current_dir = np.array([-1,0], dtype=int)
while True:
    y,x = pos
    if not 0 <= y <= max_y and 0 <= x <= max_x:
        break
    elif map[*pos] == 1:
        pos = pos - current_dir
        current_dir = dir_dict[*current_dir]
    else:
        pos_array[*pos] = 1
        if (y,x) not in guard_path and (y,x) != org_pos:
            guard_path.append((y,x))
        pos = pos + current_dir


print(int(np.sum(pos_array)))


# Task 2

key_dict = {
    (-1,0): 0,
    (0,1): 1,
    (1,0): 2,
    (0,-1): 3,
}


def check_bounds(pos, dir):
    y, x = pos + dir
    return 0 <= y <= max_y and 0 <= x <= max_x

def step(pos, dir, map):
    next_pos = pos + dir
    if map[*next_pos] == 1:
        next_dir = dir_dict[tuple(dir)]
        return pos, next_dir, False
    return next_pos, dir, True

org_pos = np.array(org_pos)
org_dir = np.array([-1,0])
def check_loop(rock_pos):
    map_copy = map.copy()
    map_copy[*rock_pos] = 1
    current_pos, current_dir, direction_array = org_pos, org_dir, np.zeros((max_y, max_x, 4))
    while check_bounds(current_pos, current_dir):
        y, x = current_pos
        next_pos, next_dir, moved = step(current_pos, current_dir, map_copy)
        dict_key = key_dict[tuple(next_dir)]
        if direction_array[y,x,dict_key]:
            return True
        else:
            if moved:
                direction_array[y,x,dict_key] = 1
                current_pos = next_pos
            current_dir = next_dir
    return False

if __name__ == '__main__':
    with Pool(8) as p:
        print(sum(p.map(check_loop, guard_path)))
    print(time.perf_counter()-start_time)

