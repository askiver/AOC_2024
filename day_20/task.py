from functools import lru_cache
from pathlib import Path
import numpy as np
from collections import defaultdict

map = [[path for path in line] for line in Path("input.txt").read_text().splitlines()]

start_pos = next((y, x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == "S")
end_pos = next((y, x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == "E")

max_y_index, max_x_index = len(map)-1, len(map[0])-1
directions = [(-1,0), (0,1), (1,0), (0,-1)]
steps_array = np.full((max_y_index+1, max_x_index+1), fill_value=np.inf)

def check_bounds(y,x):
    return 0 < y < max_y_index and 0 < x < max_x_index

def step(pos):
    y,x = pos
    for direction in directions:
        dy,dx = direction
        new_pos = y+dy, x+dx
        if check_bounds(new_pos[0], new_pos[1]):
            yield new_pos

pos = end_pos
visited = set()
steps = 0
while pos != start_pos:
    steps_array[*pos] = steps
    visited.add(pos)
    steps += 1
    for new_pos in step(pos):
        new_y, new_x = new_pos
        if new_pos not in visited and map[new_y][new_x] != "#":
            pos = new_pos
            break

max_steps = steps

@lru_cache(maxsize=None)
def find_cheats(current_pos, cheat_steps):
    y,x = current_pos

    distance_from_goal = abs(y - end_pos[0]) + abs(x - end_pos[1])
    if distance_from_goal + steps > max_steps - time_to_save:
        return set()

    num_shortcuts = {}

    if map[y][x] != "#":
        distance = org_cheat_steps - cheat_steps + steps_array[*current_pos]
        num_shortcuts[current_pos] = distance

    if cheat_steps:
        for new_pos in step(current_pos):
            new_shortcuts = find_cheats(new_pos, cheat_steps-1)

            for coord, dist in new_shortcuts:
                num_shortcuts[coord] = min(num_shortcuts.get(coord, np.inf), dist)

    num_shortcuts = {(coord, dist) for coord, dist in num_shortcuts.items()}

    return num_shortcuts


pos = start_pos
visited = set()
steps = 0
num_cheats = 0
time_to_save = 100
org_cheat_steps = 20
while pos != end_pos:
    shortcuts = find_cheats(pos, org_cheat_steps)

    for _,distance in shortcuts:
        if steps + distance <= max_steps - time_to_save:
            num_cheats += 1

    steps += 1
    y, x = pos
    visited.add(pos)

    for new_pos in step(pos):
        new_y, new_x = new_pos
        if new_pos not in visited and map[new_y][new_x] != "#":
            pos = new_pos
            break

print(num_cheats) # 1014683