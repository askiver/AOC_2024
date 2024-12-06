import time

start_time = time.perf_counter()

# Task 1
total_sum = 0
for line in open("input.txt",'r'):
    for i in range(0, len(line)-3):
        if line[i:i+4] == 'mul(':
            end_index = line[i+4:].find(')')
            if end_index > 7:
                continue
            numbers = line[i+4:i+4+end_index].split(",")
            try:
                if " " in numbers[0] or " " in numbers[1]:
                    print("test")
                    continue

                if len(numbers[0]) > 3 or len(numbers[1]) > 3:
                    continue

                number1 = int(numbers[0])
                number2 = int(numbers[1])

                total_sum += number1 * number2
            except ValueError:
                print("invalid numbers")
            except IndexError:
                print()

print(total_sum)

# Task 2

total_sum = 0
do = True
for line in open("input.txt",'r'):
    for i in range(0, len(line)-3):
        if line[i:i+4] == 'do()':
            do = True
        elif line[i:i+7] == "don't()":
            do = False
        if line[i:i+4] == 'mul(' and do:
            end_index = line[i+4:].find(')')
            if end_index > 7:
                continue
            numbers = line[i+4:i+4+end_index].split(",")
            try:
                if " " in numbers[0] or " " in numbers[1]:
                    print("test")
                    continue

                if len(numbers[0]) > 3 or len(numbers[1]) > 3:
                    continue

                number1 = int(numbers[0])
                number2 = int(numbers[1])

                total_sum += number1 * number2
            except ValueError:
                print("invalid numbers")
            except IndexError:
                print()
print(total_sum)

end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(elapsed_time)
