from pathlib import Path
import numpy as np
from collections import defaultdict

map = [[path for path in line] for line in Path("input.txt").read_text().splitlines()]

start_pos = next((y, x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == "S")
end_pos = next((y, x) for y, row in enumerate(map) for x, elem in enumerate(row) if elem == "E")

max_y_index, max_x_index = len(map)-1, len(map[0])-1

directions = [(-1,0), (0,1), (1,0), (0,-1)]

def heuristic(pos):
    y,x = pos
    end_y, end_x = end_pos
    return np.sqrt((y-end_y)**2 + (x-end_x)**2)

def check_bounds(y,x):
    return 0 < y < max_y_index and 0 < x < max_x_index

steps_array = np.full((max_y_index+1, max_x_index+1), fill_value=np.inf)

def update_steps_array(visited):
    for idx, pos in enumerate(visited[::-1]):
        steps_array[*pos] = min(steps_array[*pos], idx+1)


def find_path(cheat_steps, time_to_beat):
    shortest_path = np.inf
    possible_paths = 0
    stack = []
    cheat_dict = defaultdict(set)
    stack.append((start_pos, 0, [], cheat_steps))
    i = 0

    while stack:
        pos, steps, visited, cheat_steps_remaining = stack.pop()
        if pos == end_pos:
            possible_paths += 1
            shortest_path = min(shortest_path, steps)
            if not cheat_steps:
                update_steps_array(visited)
        elif (steps + steps_array[*pos]) < time_to_beat:
            possible_paths += 1
            shortest_path = min(shortest_path, steps + steps_array[*pos])
        elif steps_array[*pos] != np.inf and not cheat_steps and (steps + steps_array[*pos]) > time_to_beat:
            continue
        elif pos in visited or steps > time_to_beat:
            continue
        else:
            y,x = pos
            visit_copy = visited.copy()
            visit_copy.append(pos)
            for direction in directions:
                dy, dx = direction
                new_y, new_x = y + dy, x + dx
                if map[new_y][new_x] == "#":
                    if cheat and check_bounds(new_y, new_x) and map[new_y + dy][new_x + dx] != "#":
                        stack.append(((new_y+dy, new_x+dx), steps+2, visit_copy, False))
                else:
                    stack.append(((new_y,new_x), steps+1, visit_copy, cheat))
    return shortest_path, possible_paths

fastest_standard_path, _ = find_path(0, np.inf)
print(fastest_standard_path)

fastest_standard_path, number_of_fast_paths = find_path(2, fastest_standard_path-20)

print(fastest_standard_path, number_of_fast_paths)
