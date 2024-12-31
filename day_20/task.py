from functools import lru_cache
from pathlib import Path
import numpy as np
from collections import defaultdict

map = [[path for path in line] for line in Path("input.txt").read_text().splitlines()]

start_pos = next((y, x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == "S")
end_pos = next((y, x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == "E")

max_y_index, max_x_index = len(map)-1, len(map[0])-1

directions = [(-1,0), (0,1), (1,0), (0,-1)]

def check_bounds(y,x):
    return 0 < y < max_y_index and 0 < x < max_x_index

steps_array = np.full((max_y_index+1, max_x_index+1), fill_value=np.inf)

pos = end_pos
visited = []
steps = 0
while pos != start_pos:
    steps_array[*pos] = steps
    visited.append(pos)
    y,x = pos
    steps += 1
    for direction in directions:
        dy, dx = direction
        new_y, new_x = y+dy, x+dx
        new_pos = new_y, new_x

        if new_pos not in visited and map[new_y][new_x] != "#":
            pos = new_pos
            break

max_steps = steps

#cheat_dict = defaultdict(set)

@lru_cache(maxsize=None)
def find_cheats(current_pos, steps, cheat_steps, time_to_save):
    y,x = current_pos


    distance_from_goal = abs(y - end_pos[0]) + abs(x - end_pos[1])
    if distance_from_goal + steps > max_steps - time_to_save:
        return set()

    num_shorcuts = set()

    if map[y][x] != "#":
        if steps + steps_array[*current_pos] <= max_steps - time_to_save:
            num_shorcuts.add(current_pos)

    if cheat_steps:
        for direction in directions:
            dy,dx = direction
            new_pos = y+dy, x+dx
            if check_bounds(new_pos[0], new_pos[1]): # new_pos not in visited and
                new_shortcuts = find_cheats(new_pos, steps+1, cheat_steps-1, time_to_save)
                num_shorcuts.update(new_shortcuts)

    return num_shorcuts


pos = start_pos
visited = set()
steps = 0
num_cheats = 0
time_to_save = 100
cheat_steps = 20
while pos != end_pos:
    print(pos)
    num_cheats += len(find_cheats(pos, steps, cheat_steps, time_to_save))

    steps += 1
    y, x = pos
    visited.add(pos)

    for direction in directions:
        dy, dx = direction
        new_y, new_x = y + dy, x + dx
        new_pos = new_y, new_x

        if new_pos not in visited and map[new_y][new_x] != "#":
            pos = new_pos
            break

print(num_cheats) # 1014683