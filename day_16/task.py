from pathlib import Path
import heapq
import numpy as np

maze = [[path for path in row] for row in Path("input.txt").read_text().splitlines()]

start_pos = (len(maze)-2, 1)
end_pos = (1, len(maze[0])-2)
dir_dict = {(1,0): [(1,0), (0,-1), (0,1)],
            (0,1): [(0,1), (1,0), (-1,0)],
            (-1,0): [(-1,0), (0,1), (0,-1)],
            (0,-1): [(0,-1), (-1,0), (1,0)]}

best_score = np.inf

def heuristic(pos):
    start_y, start_x = pos
    end_y, end_x = end_pos
    return np.sqrt(abs(start_y-end_y)**2 + abs(start_x-end_x)**2)


score_array = np.full((len(maze), len(maze[0])), np.inf)
score_array[*start_pos] = 0
priority_queue = []
heapq.heappush(priority_queue, (np.inf, start_pos, (0,1), 0, set(), True))
travel_array = np.zeros((len(maze), len(maze[0])))

while priority_queue:

    heuristic_score, pos, current_direction, score, visited_places, bypass = heapq.heappop(priority_queue)
    if score > best_score or pos in visited_places:
        continue

    visited_places.add(pos)

    if pos == end_pos:
        best_score = score
        travel_array[*zip(*visited_places)] = 1
        continue

    y, x = pos

    for direction in dir_dict[current_direction]:
        new_score = score + 1 if direction == current_direction else score + 1001
        dy, dx = direction
        new_pos = y + dy, x + dx

        if maze[new_pos[0]][new_pos[1]] != "#":
            if new_score <= score_array[*new_pos]:
                score_array[*new_pos] = new_score
                heapq.heappush(priority_queue, (new_score + heuristic(new_pos), new_pos, direction, new_score, visited_places.copy(), True))
            elif bypass:
                heapq.heappush(priority_queue,(new_score + heuristic(new_pos), new_pos, direction, new_score, visited_places.copy(), False))

print(best_score)
print(np.sum(travel_array))