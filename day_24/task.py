from pathlib import Path
import re
import operator as op
import networkx as nx
import matplotlib.pyplot as plt
import itertools
from tqdm import tqdm

inputs, rules = Path("input.txt").read_text().split("\n\n")

input_dict = {}
for input in inputs.splitlines():
    input_dict[input[:3]] = bool(int(input[-1]))

pattern = r"(\w+)\s+(XOR|OR|AND)\s+(\w+)\s*->\s*(\w+)"
operator_dict = {"AND": op.and_, "XOR": op.xor, "OR": op.or_}

operations = []
graph = nx.DiGraph()

for rule in rules.splitlines():
    match = re.match(pattern, rule)
    if match:
        input1, operation, input2, output = match.groups()
        graph.add_edge(input1, output)
        graph.add_edge(input2, output)
        operations.append([input1, input2, operator_dict[operation], output])

plt.figure(figsize=(128,128))
pos = nx.kamada_kawai_layout(graph)  # for consistent layout
nx.draw(graph, pos, with_labels=True, node_color='lightblue', arrowstyle='->')
plt.show()

all_operations = operations.copy()

while operations:
    input1, input2, operation, output = operations.pop(0)
    if input1 in input_dict and input2 in input_dict:
        input_dict[output] = operation(input_dict.get(input1), input_dict.get(input2))
    else:
        operations.append([input1, input2, operation, output])


z_outputs = []
for key in input_dict.keys():
    if key.startswith("z"):
        z_outputs.append(key)
final_number = 0
for idx, output in enumerate(sorted(z_outputs)):
    final_number += input_dict[output] * 2**idx
print(final_number)

# Task 2

correct_dict = {}
for input in inputs.splitlines():
    input_dict[input[:3]] = bool(int(input[-1]))

correct_output = 0
for i in range(45):
    number = str(0)+str(i) if i < 10 else str(i)
    x, y = input_dict[f"x{number}"], input_dict[f"y{number}"]
    correct_output += x*2**i + y*2**i

print(correct_output)

binary_z = bin(correct_output)[2:]
for idx, value in enumerate(binary_z[::-1]):
    number = str(0) + str(idx) if idx < 10 else str(idx)
    correct_dict[f"z{number}"] = bool(int(value))
if "z45" not in correct_dict.keys():
    correct_dict["z45"] = False
#input_dict["z06"] = False

num_false_outputs = 0

for i in range(45):
    number = str(0) + str(i) if i < 10 else str(i)
    if input_dict[f"z{number}"] != correct_dict[f"z{number}"]:
        num_false_outputs += 1
print(correct_dict)
z_dict = {k: v for k, v in input_dict.items() if k.startswith("z")}
z_dict = dict(sorted(z_dict.items()))
print(z_dict)
print(num_false_outputs)
