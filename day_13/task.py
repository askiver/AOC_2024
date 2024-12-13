import re
import numpy as np
from scipy.optimize import linprog

# Read and parse input data
with open('input.txt') as f:
    data = f.read()

pattern = re.compile(r'X[+=](\d+), Y[+=](\d+)')
result = [tuple(tuple(map(int, match)) for match in pattern.findall(block))
          for block in data.strip().split('\n\n') if len(pattern.findall(block)) == 3]

big_number = 10000000000000

# Objective: Minimize total button presses
lowest_token = 0
lowest_big_token = 0

for results in result:
    # Extract coefficients and target values
    X_coefficients = [results[0][0], results[1][0]]
    Y_coefficients = [results[0][1], results[1][1]]
    coefficients = np.array([X_coefficients, Y_coefficients])
    answers = np.array([results[2][0], results[2][1]])

    # Solve for the small calculation using linprog
    c = np.array([3, 1])  # Coefficients for the objective function
    bounds = [(0, None), (0, None)]  # Non-negative bounds for variables
    res = linprog(c, A_eq=coefficients, b_eq=answers, bounds=bounds, method='highs')

    if res.success:
        a_press, b_press = np.ceil(res.x).astype(int)
        lowest_token += 3 * a_press + b_press
    else:
        print("No solution for small calculation.")

    # Solve for the big calculation using linprog
    answers_big = answers + big_number
    res_big = linprog(c, A_eq=coefficients, b_eq=answers_big, bounds=bounds, method='highs')

    if res_big.success:
        a_press_big, b_press_big = np.ceil(res_big.x).astype(int)
        lowest_big_token += 3 * a_press_big + b_press_big
    else:
        print("No solution for big calculation.")

# Print results
print(lowest_token)
print(lowest_big_token)
