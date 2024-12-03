# Task 1
reports = []
for line in open("input.txt", 'r'):
    levels = [int(level) for level in line.split(" ")]
    reports.append(levels)

def find_valid_report(report):
    if not (sorted(report) == report or sorted(report, reverse=True) == report) or len(report) != len(set(report)):
        return 0
    for i in range(0, len(report)-1):
        if abs(report[i]-report[i+1]) > 3:
            return 0
    return 1
print(reports)
valid = 0
for report in reports:
    valid += find_valid_report(report)

print(valid)

# Task 2

valid = 0
for report in reports:
    if find_valid_report(report) == 0:
    # Try removing elements and see if that makes things work
        for i in range(0, len(report)):
            part_report = report.copy()
            del part_report[i]
            if find_valid_report(part_report) == 1:
                valid +=1
                break
    else:
        valid += 1

print(valid)
