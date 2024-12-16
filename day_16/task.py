import copy
from pathlib import Path
import math
from collections import deque
import sys


# Increase recursion limit
sys.setrecursionlimit(10000)

maze = Path("input.txt").read_text()

maze = [[path for path in row] for row in maze.splitlines()]
dir_dict = {(1,0): [(1,0), (0,-1), (0,1)],
            (0,1): [(0,1), (1,0), (-1,0)],
            (-1,0): [(-1,0), (0,1), (0,-1)],
            (0,-1): [(0,-1), (-1,0), (1,0)]}

"""
def traverse_maze(pos, current_direction, score, best_score, visited_places):
    if pos in visited_places or score > best_score:
        return math.inf

    visited_places.add(pos)
    y,x = pos
    if maze[y][x] == "E":
        visited_places.remove(pos)
        return score

    best_path_score = math.inf
    for direction in dir_dict[current_direction]:
        new_score = score + 1 if direction == current_direction else score + 1001
        dy,dx = direction
        new_pos = (y+dy, x+dx)
        if maze[new_pos[0]][new_pos[1]] != "#":
            best_path_score = min(best_path_score, traverse_maze(new_pos, direction, new_score, best_path_score, visited_places))

    visited_places.remove(pos)
    return best_path_score
"""
start_pos = (len(maze)-2, 1)
best_score = math.inf
#print(traverse_maze(start_pos, (0,1), 0, math.inf, set()))
stack = deque()
stack.append((start_pos, (0,1), 0, set()))
i = 0
while len(stack) > 0:

    if i % 100000 == 0:
        print(len(stack))

    pos, current_direction, score, visited_places = stack.pop()
    if pos in visited_places or score > best_score:
        continue

    y,x = pos
    if maze[y][x] == "E":
        best_score = min(best_score, score)
        continue
    visited_places.add(pos)
    for direction in dir_dict[current_direction]:
        new_score = score + 1 if direction == current_direction else score + 1001
        dy, dx = direction
        new_pos = (y + dy, x + dx)
        if maze[new_pos[0]][new_pos[1]] != "#":
            stack.append((new_pos, direction, new_score, copy.copy(visited_places)))


print(best_score)



