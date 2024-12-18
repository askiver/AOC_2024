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

best_score = 10**5

def traverse_maze(pos, current_direction, score):
    global best_score

    if score > best_score:
        return np.inf

    if pos==end_pos:
        return score

    return_score = np.inf
    heuristics = []
    args = []
    y,x = pos
    for direction in dir_dict[current_direction]:
        new_score = score + 1 if direction == current_direction else score + 1001
        dy,dx = direction
        new_pos = (y+dy, x+dx)
        if maze[new_pos[0]][new_pos[1]] != "#":
            args.append((new_pos, direction, new_score))
            heuristics.append(heuristic(new_pos))
    for index, value in sorted(enumerate(heuristics), key=lambda x: x[1]):
        new_pos, direction, new_score = args[index]
        score_result = traverse_maze(new_pos, direction, new_score)
        if score_result <= best_score:
            best_score = score_result
            score_array[*pos] = score if direction == current_direction else score + 1000
            return_score = score_result
    return return_score

def heuristic(pos):
    start_y, start_x = pos
    end_y, end_x = end_pos
    return np.sqrt(abs(start_y-end_y)**2 + abs(start_x-end_x)**2)

score_array = np.zeros((len(maze), len(maze[0])))
score_array.fill(np.inf)
score_array[*start_pos] = 0

priority_queue = []
heapq.heappush(priority_queue, (np.inf, start_pos, (0,1), 0))
"""
while priority_queue:

    heuristic_score, pos, current_direction, score =heapq.heappop(priority_queue)
    if score > best_score or score > score_array[*pos]:
        continue

    if pos == end_pos:
        best_score = min(best_score, score)
        continue

    y, x = pos

    for direction in dir_dict[current_direction]:
        new_score = score + 1 if direction == current_direction else score + 1001
        dy, dx = direction
        new_pos = (y + dy, x + dx)

        if maze[new_pos[0]][new_pos[1]] != "#" and score_array[*new_pos] >= new_score:
            score_array[*new_pos] = new_score
            heapq.heappush(priority_queue,(new_score + heuristic(new_pos), new_pos, direction, new_score))

"""
print(traverse_maze(start_pos, (0,1), 0))
print(best_score)

# Task 2
travel_array = np.zeros((len(maze), len(maze[0])))
def find_best_neighbour(pos, score):
    y,x = pos
    for direction in directions:
        dy,dx = direction
        neighbour = y+dy, x+dx
        if score_array[*neighbour] == score:
            return neighbour


def find_num_tiles(pos):
    travel_array[*pos] = 1
    if pos == start_pos:
        return
    elif pos == end_pos:
        find_num_tiles(find_best_neighbour(end_pos, best_score-1))

    else:
        score = score_array[*pos]
        y, x = pos
        for direction in directions:
            dy,dx = direction
            neighbour = y+dy, x+dx
            if score_array[*neighbour] < score:
                find_num_tiles(neighbour)

find_num_tiles(end_pos)

print(np.sum(travel_array))
