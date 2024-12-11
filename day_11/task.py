from os import remove
from pathlib import Path
from tqdm import tqdm
from functools import lru_cache
import time

start_time = time.perf_counter()

org_stones = Path("input.txt").read_text().strip()
stones = org_stones.split(" ")

def morph_stone(stone):
    length = len(stone)
    if length %2 == 0:
        halfway = length // 2
        return str(int(stone[:halfway])), str(int(stone[halfway:]))
    if stone == "0":
        return "1",
    return str(int(stone)*2024),

@lru_cache(maxsize=None)
def recursive_stones(stone, depth):
    if not depth:
        return 1
    else:
        morphed_stones = morph_stone(stone)
        length = 0
        for morphed_stone in morphed_stones:
            length += recursive_stones(morphed_stone, depth - 1)
        return length

depths = (25,75)
for depth in depths:
    total_stones = 0
    for stone in stones:
        total_stones += recursive_stones(stone, depth)
    print(total_stones)

print(time.perf_counter()-start_time)


