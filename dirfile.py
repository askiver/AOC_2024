import os
for i in range(1,26):
    os.makedirs(f"day_{i}", exist_ok=True)
    with open(f"day_{i}/input.txt", "w") as file:
        file.write("")
    with open(f"day_{i}/task.py", "w") as file:
        file.write("")