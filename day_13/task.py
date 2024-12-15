import re

# Read and parse input data
with open('input.txt') as f:
    data = f.read()

# Parse the input data
def parse_input(data):
    pattern = re.compile(r'X[+=](\d+), Y[+=](\d+)')
    return [
        tuple(tuple(map(int, match)) for match in pattern.findall(block))
        for block in data.strip().split('\n\n')
        if len(pattern.findall(block)) == 3
    ]

def find_presses(button_A, button_B, answers):
    ax, ay = button_A
    bx, by = button_B
    zx, zy = answers

    A = (bx * zy - by * zx) / (bx * ay - ax * by)
    B = (zx - ax * A) / bx

    if 0 < A and 0 < B:
        if int(A) == A and int(B) == B:
            return 3*A + B

    return 0


result = parse_input(data)
big_number = 10000000000000
token_count = 0
big_tokens = 0
for results in result:
    # Example equations
    # 94A + 22B = 8400
    # 34A + 67B = 5400
    # B = (8400 - 94A) / 22
    # 34A + 67((8400-94A)/22) = 5400
    # 22*34A + 67*(8400-94A) = 22*5400
    # A(22*34-94*67) = 22*5400-67*8400
    # A = (22*5400-67*8400) / (22*34-94*67)
    # A = (bx*zy - by*zx) / (bx*ay-ax*by)
    # B = (8400 - 94A) / 22
    # B = (zx - ax*A) / bx

    button_A, button_B, answers = results

    token_count += find_presses(button_A, button_B, answers)

    answers = (answers[0] + big_number, answers[1] + big_number)
    big_tokens += find_presses(button_A, button_B, answers)

print(token_count)
print(big_tokens)