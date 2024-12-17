from pathlib import Path
import heapq
import numpy as np
import sys

sys.setrecursionlimit(10**6)


maze = Path("input.txt").read_text()

maze = [[path for path in row] for row in maze.splitlines()]
start_pos = (len(maze)-2, 1)
end_pos = (1, len(maze[0])-2)
directions = [(1,0), (0,1), (-1,0), (0,-1)]
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
def heuristic(pos):
    start_y, start_x = pos
    end_y, end_x = end_pos
    return np.sqrt(abs(start_y-end_y)**2 + abs(start_x-end_x)**2)

score_array = np.zeros((len(maze), len(maze[0])))
score_array.fill(np.inf)
best_score = np.inf
#print(traverse_maze(start_pos, (0,1), 0, math.inf, set()))
priority_queue = []
heapq.heappush(priority_queue, (np.inf, start_pos, (0,1), 0))
i = 0
while priority_queue:
    i+= 1
    if i % 10000 == 0:
        print(len(priority_queue))

    heuristic_score, pos, current_direction, score =heapq.heappop(priority_queue)
    if score > best_score or score > score_array[*pos]:
        continue

    y, x = pos
    if maze[y][x] == "E":
        best_score = min(best_score, score)
        continue

    for direction in dir_dict[current_direction]:
        new_score = score + 1 if direction == current_direction else score + 1001
        dy, dx = direction
        new_pos = (y + dy, x + dx)

        if maze[new_pos[0]][new_pos[1]] != "#" and score_array[*new_pos] > new_score:
            score_array[*new_pos] = new_score
            heapq.heappush(priority_queue,(new_score + heuristic(new_pos), new_pos, direction, new_score))


print(best_score)

# Task 2

def find_num_tiles(pos):
    if pos == start_pos:
        return 1
    else:
        best_neighbour = None
        best_score = np.inf
        y, x = pos
        for direction in directions:
            dy,dx = direction
            neighbour = y+dy, x+dx
            if score_array[*neighbour] < best_score:
                best_score = score_array[*neighbour]
                best_neighbour = neighbour

        return 1 + find_num_tiles(best_neighbour)

print(find_num_tiles(end_pos))
