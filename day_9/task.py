from pathlib import Path
from tqdm import tqdm

disk = Path("input.txt").read_text()

print(disk)
puzzle = []
# Create puzzle
block_number = 0
for index, amount in enumerate(disk):
    if index % 2 == 0:
        for i in range(int(amount)):
            puzzle.append(block_number)
        block_number += 1
    else:
        for i in range(int(amount)):
            puzzle.append(-1)

for index, number in enumerate(puzzle):
    if number == -1:
        if all(x == -1 for x in puzzle[index:]):
            break
        else:
            for i in range(len(puzzle) - 1, -1, -1):
                if puzzle[i] != -1:
                    puzzle[i], puzzle[index] = puzzle[index], puzzle[i]
                    break
checksum = 0
for index, number in enumerate(puzzle):
    if number == -1:
        break
    checksum += index * number


def find_block_length(index, number):
    current_count = 1
    relevant_puzzle = puzzle[index:]
    for i in range(1, len(relevant_puzzle)):
        if relevant_puzzle[i] == number:
            current_count += 1
        else:
            break
    return current_count

print(puzzle)
print(checksum)

puzzle = []

block_number = 0
for index, amount in enumerate(disk):
    if index % 2 == 0:
        for i in range(int(amount)):
            puzzle.append(block_number)
        block_number += 1
    else:
        for i in range(int(amount)):
            puzzle.append(-1)


print(puzzle)

for i in range(max(puzzle), 1, -1):
    index = puzzle.index(i)
    block_length = find_block_length(index, i)
    blank_index = 0
    relevant_puzzle = puzzle[blank_index:]
    while len(relevant_puzzle) > 0:
        nearest_blank = relevant_puzzle.index(-1)
        blank_block_length = find_block_length(blank_index + nearest_blank, -1)

        if blank_index + nearest_blank > index:
            break

        if blank_block_length >= block_length:
            puzzle[blank_index + nearest_blank:blank_index + nearest_blank + block_length] = [i] * block_length
            puzzle[index:index + block_length] = [-1] * block_length
            break
        else:
            blank_index += nearest_blank + blank_block_length
            relevant_puzzle = puzzle[blank_index:]


checksum = 0
for index, number in enumerate(puzzle):
    if number == -1:
        continue
    checksum += index * number

#print(puzzle)
#print(len(puzzle))
print(checksum)


