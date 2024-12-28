from pathlib import Path
import numpy as np

value_dict = {"#": 1, ".": 0}
data = Path("input.txt").read_text().split("\n\n")

locks = []
keys = []

for item in data:
    relevant_list = locks if item[0] == "#" else keys
    relevant_list.append([[value_dict[value] for value in row] for row in item.split("\n")])

locks, keys = np.array(locks), np.array(keys)
len_y, len_x = len(locks[0]), len(locks[0][0])

lock_sum, key_sum = np.sum(locks, axis=1), np.sum(keys, axis=1)

print(lock_sum)

lock_key_combos = 0
for lock in lock_sum:
    for key in key_sum:
        if not np.any(key+lock > 7):
            lock_key_combos += 1

print(lock_key_combos)