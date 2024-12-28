from pathlib import Path
from functools import lru_cache

codes = Path("input.txt").read_text().splitlines()

directions = {(-1,0): "^", (0,1): ">", (1,0): "v", (0,-1): "<"}
directional_keypad = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}
numeric_keypad = {"0": (3,1), "A": (3,2)}
for row, i in enumerate(range(2, -1, -1)):
    for column, j in enumerate(range(1,4)):
        numeric_keypad[str(i*3 + j)] = (row,column)


def find_instructions(keypad, code, pos=None):
    current_pos = keypad["A"] if pos is None else keypad[pos]
    commands = []
    for button in code:
        wanted_pos = keypad[button]
        dy,dx = tuple(x - y for x, y in zip(wanted_pos, current_pos))

        y,x = current_pos
        dy_sign = (dy // abs(dy) if dy != 0 else 0)
        dx_sign = (dx // abs(dx) if dx != 0 else 0)
        positions = keypad.values()
        while dy or dx:
            if dx < 0 and (y, x+dx) in positions:
                while dx:
                    x += dx_sign
                    dx -= dx_sign
                    commands.append(directions.get((0, dx_sign)))
            elif dy and (y+dy, x) in positions:
                while dy:
                    y += dy_sign
                    dy -= dy_sign
                    commands.append(directions.get((dy_sign, 0)))

            else:
                while dx:
                    x += dx_sign
                    dx -= dx_sign
                    commands.append(directions.get((0, dx_sign)))

        commands.append("A")
        current_pos = keypad[button]

    return commands


@lru_cache(maxsize=None)
def find_robot_instructions(depth, max_depth, move, pos):
    if depth == max_depth:
        return 1

    moves = find_instructions(directional_keypad, [move], pos)
    last_move = None
    sequence_length = 0
    for move in moves:
        sequence_length += find_robot_instructions(depth+1, max_depth, move, last_move)
        last_move = move

    return sequence_length


def complexity(sequence_length, original_code):
    numerical_score = int(original_code[:-1])
    return sequence_length * numerical_score

num_robots = [2,25]
for depth in num_robots:
    complexity_score = 0
    for original_code in codes:
        last_move = "A"
        code = find_instructions(numeric_keypad, original_code)
        sequence_length = 0
        for move in code:
            sequence_length += find_robot_instructions(0, depth, move, last_move)
            last_move = move

        complexity_score += complexity(sequence_length, original_code)

    print(complexity_score)