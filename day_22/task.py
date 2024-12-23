from pathlib import Path
import sys
from tqdm import tqdm
from itertools import product

sys.setrecursionlimit(3000)

initial_secrets = [int(secret) for secret in Path("input.txt").read_text().splitlines()]
prune = 16777216
all_secrets = []

def calculate_secret(secret):
    secret = ((secret * 64) ^ secret) % prune
    secret = ((secret // 32) ^ secret) % prune
    return ((secret * 2048) ^ secret) % prune


def find_secret(secret, depth, local_secrets):
    if depth == 0:
        all_secrets.append(local_secrets)
        return secret
    secret = calculate_secret(secret)
    local_secrets.append(secret)
    return find_secret(secret, depth-1, local_secrets)

total_sum = 0
for secret in initial_secrets:
    total_sum += find_secret(secret, 2000, [secret])

print(total_sum)
print(len(all_secrets))
print(len(all_secrets[0]))
# Task 2

def find_sublist(lst, sublst):
    # Use a separator unlikely to appear in the string representation of numbers
    separator = "|"

    # Convert both lists to strings with the chosen separator
    lst_str = separator + separator.join(map(str, lst)) + separator
    sublst_str = separator + separator.join(map(str, sublst)) + separator

    # Find the sublist as a substring
    idx = lst_str.find(sublst_str)

    if idx == -1:
        return -1  # Sublist not found

    # Calculate the starting index of the match
    return lst_str[:idx].count(separator) + len(sublst)

def verify_sequence(sequence):
    total_value = sequence[0]
    for value in sequence[1:]:
        total_value += value
        if total_value < -9 or total_value > 9:
            return False
    return True

# Find all changes for the secrets
changes = []
for secret in all_secrets:
    previous_value = secret[0] % 10
    local_changes = []
    for j in range(1, 2001):
        current_value = secret[j] % 10
        local_changes.append(current_value - previous_value)
        previous_value = current_value
    changes.append(local_changes)

all_sequences = product(range(-9,10), repeat=4)
highest_banana_count = 0
best_sequence = None

for sequence in tqdm(all_sequences, total=19**4):
    if not verify_sequence(sequence):
        continue
    local_bananas = 0

    for idx, change in enumerate(changes):
        if highest_banana_count > (2000-idx)*9: # can't beat the highest score
            break
        sublist_idx = find_sublist(change, sequence)
        if sublist_idx != -1:
            local_bananas += all_secrets[idx][sublist_idx] % 10


    highest_banana_count = max(highest_banana_count, local_bananas)


print(highest_banana_count)
print(best_sequence)

