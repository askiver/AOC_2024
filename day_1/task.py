# Task 1
left_list = []
right_list = []
for line in open("input.txt",'r'):
    numbers = line.split("   ")
    left_list.append(int(numbers[0]))
    right_list.append(int(numbers[1]))

left_list.sort()
right_list.sort()
distance = 0
for left, right in zip(left_list, right_list):
    distance += abs(left-right)

print(distance)

# Task 2

from collections import defaultdict

dict = defaultdict(int)

for number in right_list:
    dict[number] += 1

similarity=0
for number in left_list:
    similarity += number * dict[number]

print(similarity)



