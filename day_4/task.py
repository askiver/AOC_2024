all_lines = []
for line in open('input.txt', 'r'):
    all_lines.append(line.strip())

# Task 1
directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1))
xmas = "XMAS"
max_y = len(all_lines) - 1
max_x = len(all_lines[0]) - 1

def check_xmas(pos, dir, depth):
    y,x = pos[0], pos[1]
    if not all_lines[y][x] == xmas[depth]:
        return 0
    if depth == 3:
        return 1
    new_pos = [position + direction for position, direction in zip(pos, dir)]
    y, x = new_pos[0], new_pos[1]
    if x > max_x or y > max_y or x < 0 or y < 0:
        return 0
    return check_xmas((y,x), dir, depth + 1)

total_words = 0
for y in range(max_y+1):
    for x in range(max_x+1):
        for dir in directions:
            total_words += check_xmas((y,x), dir, 0)

print(total_words)

# Task 2
mas = "MASM"
x_mas_directions = ((1,1), (-1,1), (1,-1), (-1,-1))

duo_dict = {}
duo_dict[(1,1)] = ((0,2),(1,-1)) # Check top right m for top left
duo_dict[(-1,1)] = ((-2,0),(1,1)) # Check top left m for bottom left
duo_dict[(1,-1)] = ((2,0), (-1,-1)) # Check bottom right m for top right
duo_dict[(-1,-1)] = ((0,-2), (-1,1)) # check bottom left m for bottom right


def check_xmas2(pos,dir,depth):
    y, x = pos[0], pos[1]
    if x > max_x or y > max_y or x < 0 or y < 0:
        return False
    if depth == -1 and all_lines[y][x] == "M":
        pos_offset, alt_dir = duo_dict[dir]

        new_alt_pos = [org_pos + position for org_pos, position in zip(pos, pos_offset)]
        new_pos = [position + direction for position, direction in zip(pos, dir)]
        if check_xmas2(new_pos, dir,1) and check_xmas2(new_alt_pos, alt_dir, 0):
            return True
        return False

    if not all_lines[y][x] == mas[depth]:
        return False
    if depth == 2:
        return True

    new_pos = [position + direction for position, direction in zip(pos, dir)]
    return check_xmas2(new_pos, dir, depth + 1)


total_x_mas = 0
for y in range(max_y + 1):
    for x in range(max_x + 1):
        for dir in x_mas_directions:
            total_x_mas += check_xmas2((y, x), dir, -1)

print(total_x_mas)


