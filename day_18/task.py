from pathlib import Path
import heapq
import numpy as np
data = Path("input.txt").read_text()

corrupted_memory = [[int(y)+1, int(x)+1] for line in data.splitlines() for x, y in [line.split(",")]]

def corrupt_memory(stop_idx):
    map = np.ones((73, 73))
    for idx, pos in enumerate(corrupted_memory):
        map[*pos] = 0
        if idx == stop_idx:
            break
    map[0, :] = 0  # Top edge
    map[-1, :] = 0  # Bottom edge
    map[:, 0] = 0  # Left edge
    map[:, -1] = 0  # Right edge
    return map

map = corrupt_memory(1023)
directions = [(1,0), (0,1), (-1,0), (0,-1)]
max_y, max_x = len(map), len(map[0])
start_pos = (1,1)
end_pos = (max_y-2, max_x-2)

def heuristic(pos):
    start_y, start_x = pos
    end_y, end_x = end_pos
    return np.sqrt(abs(start_y-end_y)**2 + abs(start_x-end_x)**2)

steps_array = np.full((max_y-1, max_x-1), np.inf)
def A_star(map, steps_array):
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic(start_pos), start_pos, 0))
    while priority_queue:

        heuristic_score, pos, steps = heapq.heappop(priority_queue)
        if steps > steps_array[*pos]:
            continue
        if pos == end_pos:
            return steps

        new_steps = steps + 1
        y,x = pos
        for direction in directions:
            dy,dx = direction
            new_pos = y+dy, x+dx
            if map[*new_pos] and new_steps < steps_array[*new_pos]:
                steps_array[*new_pos] = new_steps
                heapq.heappush(priority_queue, (new_steps + heuristic(new_pos), new_pos, new_steps))

print(A_star(map, steps_array))

# Task 2
# Do a bisect search of which byte index will result in no path being possible
possible_index = 0
impossible_index = len(corrupted_memory)-1

while impossible_index - possible_index > 1:
    steps_array = np.full((max_y-1, max_x-1), np.inf)
    current_index = ((impossible_index - possible_index) // 2) + possible_index
    map = corrupt_memory(current_index)
    steps_required = A_star(map,np.copy(steps_array))

    if not steps_required:
        impossible_index = current_index
    else:
        possible_index = current_index

end_byte = corrupted_memory[impossible_index]
y,x = end_byte[0] -1, end_byte[1] -1

print(f"{x},{y}")

