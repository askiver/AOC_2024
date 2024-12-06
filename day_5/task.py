from collections import defaultdict
import time

# Task 1
order_dict = defaultdict(list)
pages = []
rules = True
for line in open('input.txt', 'r'):
    if line == "\n":
        rules = False
    elif rules:
        stripped_line = line.strip()
        rule = [int(value) for value in stripped_line.split("|")]
        order_dict[rule[0]].append(rule[1])
    else:
        stripped_line = line.strip()
        page = [int(value) for value in stripped_line.split(",")]
        pages.append(page)

start_time = time.perf_counter()



def check_page(page):
    for idx, value in enumerate(page):
        for rule in order_dict[value]:
            if rule in page[:idx]:
                return 0
    return page[len(page)//2]

total_pages = 0
for page in pages:
    total_pages += check_page(page)

print(total_pages)

middle_time = time.perf_counter()

print(middle_time-start_time)
# Task 2

def fix_incorrect_page(page):
    if check_page(page) == 0:
        fixed_page = []
        for value in page:
            if len(fixed_page) == 0:
                fixed_page.append(value)
            else:
                for idx in range(len(fixed_page), -1, -1):
                    new_fixed_page = fixed_page.copy()
                    new_fixed_page.insert(idx, value)
                    if check_page(new_fixed_page) != 0:
                        fixed_page = new_fixed_page
                        break
        return fixed_page[len(fixed_page)//2]
    return 0

total_wrong_pages = 0
for page in pages:
    total_wrong_pages += fix_incorrect_page(page)

print(total_wrong_pages)

end_time = time.perf_counter()

print(end_time-start_time)
