from pathlib import Path
import re
import operator
from itertools import product

data = Path("input.txt").read_text().splitlines()
data = [[int(s) for s in re.split(": | ", e)] for e in data]

def add_numbers(num1, num2):
    return int(str(num1)+str(num2))

all_operators = [operator.add, operator.mul]

def check_if_possible(equation):
    answer = equation[0]
    operands = equation[1:]
    all_combinations = list(product(all_operators, repeat=len(operands)-1))
    for combination in all_combinations:
        result = combination[0](*operands[0:2])
        for j in range(2, len(operands)):
            op = combination[j-1]
            result = op(result,operands[j])
        if result == answer:
            return result
    return 0

# Task 1
total_sum = 0
for equation in data:
    total_sum += check_if_possible(equation)
print(total_sum)

# Task 2
total_sum = 0
all_operators.append(add_numbers)
for equation in data:
    total_sum += check_if_possible(equation)
print(total_sum)
