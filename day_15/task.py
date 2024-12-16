from pathlib import Path
import numpy as np

objects = []
moves = []
current_list = objects
data = Path("input.txt").read_text()

for line in data.splitlines():
    if line == "":
        current_list = moves
        continue
    current_list.append([obstacle for obstacle in line])

height = len(objects)
width = len(objects[0])
obstacle_array = np.zeros((height, width))
org_pos = None


obstacle_dict = {"#":-1, ".":0, "O":1, "[":2, "]":3}
move_dict = {"^": np.array([-1,0]), ">": np.array([0,1]), "v": np.array([1,0]), "<": np.array([0,-1])}
for y in range(height):
    for x in range(width):
        current_obstacle = objects[y][x]
        if current_obstacle == "@":
            org_pos = y,x
        else:
            obstacle_array[y,x] = obstacle_dict[current_obstacle]
moves = [move for sublist in moves for move in sublist]

robot_pos = np.array([*org_pos])

def move_allowed(pos, direction, map):
    if map[*pos] == -1:
        return False
    elif map[*pos] == 0:
        return True
    else:
        new_pos = pos + direction
        can_move = move_allowed(new_pos, direction, map)
        if can_move:
            map[*new_pos] = map[*pos]
            return True
        return False

for move in moves:
    direction = move_dict[move]
    if move_allowed(robot_pos + direction, direction, obstacle_array):
        robot_pos += direction
        obstacle_array[*robot_pos] = 0

y,x = np.where(obstacle_array == 1)
print(np.sum(y*100 + x))


# Task 2
wide_robot_pos = np.array([org_pos[0], org_pos[1]*2])
wide_obstacle_array = np.zeros((height, width*2), dtype=int)
for y in range(height):
    for x in range(width):
        current_obstacle = objects[y][x]
        if current_obstacle == "O":
            wide_obstacle_array[y,x*2] = 2
            wide_obstacle_array[y, x*2 +1] = 3
        elif current_obstacle == "#":
            wide_obstacle_array[y,x*2:x*2 + 2] = -1

wide_obstacle_dict = {2: np.array([0,1]), 3: np.array([0,-1])}
def wide_move_allowed(pos, direction, map):
    if map[*pos] == -1:
        return False
    if map[*pos] == 0:
        return True
    new_pos = pos + direction
    other_side_move = wide_obstacle_dict[int(map[*pos])]
    other_side_pos = pos + other_side_move
    can_move = (wide_move_allowed(new_pos, direction, map) and
                wide_move_allowed(other_side_pos + direction, direction, map))
    if can_move:
        left_index = min(pos[1], other_side_pos[1])
        map[new_pos[0], left_index:left_index+2] = [2,3]
        map[pos[0], left_index:left_index+2] = [0,0]
        return True
    else:
        return False

for move in moves:
    direction = move_dict[move]
    array_copy = np.copy(wide_obstacle_array)
    move_function = move_allowed if direction[1] else wide_move_allowed
    if move_function(wide_robot_pos + direction, direction, wide_obstacle_array):
        wide_robot_pos += direction
        wide_obstacle_array[*wide_robot_pos] = 0
    else:
        wide_obstacle_array = array_copy

y,x = np.where((wide_obstacle_array[:, :-1] == 2) & (wide_obstacle_array[:, 1:] == 3))
print(np.sum(y*100 + x))