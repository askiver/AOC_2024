from pathlib import Path
from functools import lru_cache

data = Path("input.txt").read_text()
towels_data, onsens_data = data.split("\n\n")
towels = set(towel.strip() for towel in towels_data.split(","))
onsens = [line.strip() for line in onsens_data.splitlines()]
towel_lengths = sorted(set(len(towel) for towel in towels))
longest_towel = max((len(towel) for towel in towels), default=0)

@lru_cache(maxsize=None)
def find_towel_combos(onsen):
    if not onsen:
        return 1
    num_combos = 0
    for towel_length in towel_lengths:
        if towel_length > len(onsen):
            break
        if onsen[:towel_length] in towels:
            num_combos += find_towel_combos(onsen[towel_length:])
    return num_combos

num_onsens = 0
num_combos = 0

for onsen in onsens:
    local_combos = find_towel_combos(onsen)
    num_onsens += bool(local_combos)
    num_combos += local_combos

print(num_onsens)
print(num_combos)