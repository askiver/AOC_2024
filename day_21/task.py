from pathlib import Path

codes = [code for code in Path("input.txt").read_text().splitlines()]

directions = {(-1,0): "^", (0,1): ">", (1,0): "v", (0,-1): "<"}
directional_keypad = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}
numeric_keypad = {"0": (3,1), "A": (3,2)}
for row, i in enumerate(range(2, -1, -1)):
    for column, j in enumerate(range(1,4)):
        numeric_keypad[str(i*3 + j)] = (row,column)

def find_instructions(keypad:dict, code):
    current_pos = keypad["A"]
    commands = []
    for button in code:
        wanted_pos = keypad[button]
        dy,dx = tuple(x - y for x, y in zip(wanted_pos, current_pos))

        y,x = current_pos
        dy_sign = (dy // abs(dy) if dy != 0 else 0)
        dx_sign = (dx // abs(dx) if dx != 0 else 0)
        positions = keypad.values()
        while dy or dx:
            if dx and (y, x+dx) in positions:
                for x_change in range(abs(dx)):
                    x += dx_sign
                    dx -= dx_sign
                    commands.append(directions.get((0, dx_sign)))

            if dy:
                for y_change in range(abs(dy)):
                    y += dy_sign
                    dy -= dy_sign
                    commands.append(directions.get((dy_sign, 0)))

        commands.append("A")
        current_pos = keypad[button]

    return commands

def complexity(full_code, original_code):
    sequence_length = len(full_code)
    numerical_score = int(original_code[:-1])
    return sequence_length * numerical_score

complexity_score = 0
for original_code in codes:
    code = original_code
    for robot in range(3):
        keypad = numeric_keypad if not robot else directional_keypad
        new_code = find_instructions(keypad, code)
        code = new_code
    complexity_score += complexity(code, original_code)

print(complexity_score)


