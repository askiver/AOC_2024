from pathlib import Path
from functools import lru_cache

stones = Path("input.txt").read_text().strip().split(" ")

@lru_cache(maxsize=None)
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
        return sum([recursive_stones(morphed, depth-1) for morphed in morph_stone(stone)])

depths = (25,75)
for depth in depths:
    total_stones = sum(recursive_stones(stone, depth) for stone in stones)
    print(total_stones)
