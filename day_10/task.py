from pathlib import Path
import numpy as np
import time

start_time = time.perf_counter()

data = Path("input.txt").read_text()

map = np.array([[int(number) for number in line] for line in data.splitlines()])
max_y, max_x = len(map), len(map[0])
directions = [(-1,0), (0,1), (1,0), (0,-1)]

def check_trailhead(y,x, previous_value, visited_tops):
    if 0 <= y < max_y and 0 <= x < max_x:
        current_value = map[y,x]
        if current_value == previous_value + 1:
            if current_value == 9:
                if (y,x) not in visited_tops:
                    visited_tops.append((y,x))
                    return 1

            else:
                trailheads = 0
                for direction in directions:
                    dy,dx = direction
                    trailheads += check_trailhead(y + dy, x+dx, current_value, visited_tops)
                return trailheads
    return 0

total_trailheads = 0
hike_starts = np.where(map == 0)

for y,x in zip(*hike_starts):
    visited_tops = []
    for direction in directions:
        dy, dx = direction
        total_trailheads+= check_trailhead(y + dy,x + dx, 0, visited_tops)

print(total_trailheads)
#
def check_trailhead(y,x, previous_value):
    if 0 <= y < max_y and 0 <= x < max_x:
        current_value = map[y,x]
        if current_value == previous_value + 1:
            if current_value == 9:
                return 1

            else:
                trailheads = 0
                for direction in directions:
                    dy,dx = direction
                    trailheads += check_trailhead(y + dy, x+dx, current_value)
                return trailheads
    return 0

total_rating = 0
for y,x in zip(*hike_starts):
    for direction in directions:
        dy, dx = direction
        total_rating+= check_trailhead(y + dy,x + dx, 0)

print(total_rating)
print(time.perf_counter()-start_time)