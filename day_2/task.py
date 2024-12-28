from pathlib import Path

# Task 1

reports = [[int(level) for level in row.split(" ")] for row in Path("input.txt").read_text().splitlines()]

def find_valid_report(report):
    if not (sorted(report) == report or sorted(report, reverse=True) == report) or len(report) != len(set(report)):
        return 0
    for i in range(0, len(report)-1):
        if abs(report[i]-report[i+1]) > 3:
            return 0
    return 1

valid = 0
for report in reports:
    valid += find_valid_report(report)

print(valid)

# Task 2

valid = 0
for report in reports:
    for i in range(0, len(report)):
        part_report = report.copy()
        del part_report[i]
        if find_valid_report(part_report) == 1:
            valid +=1
            break

print(valid)
