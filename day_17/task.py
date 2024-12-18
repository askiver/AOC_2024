from pathlib import Path
import multiprocessing

program = Path("input.txt").read_text()

current_register = "A"

registers = {}

for line in program.splitlines():
    if line.startswith("Register"):
        _, value = line.split(":")
        registers[current_register] = int(value.strip())
        current_register = chr(ord(current_register) + 1)
    elif line.startswith("Program"):
        _, instructions = line.split(":")
        instructions = [int(instruction) for instruction in instructions.strip() if instruction.isdigit()]

def is_strict_int(value):
    return isinstance(value, int) and not isinstance(value, bool)

def combo_operands(number):
    if number < 4:
        return number
    else:
        character = chr(65 + (number-4))
        return registers.get(character)

def adv(operand):
    registers["A"] =  registers.get("A") // 2**combo_operands(operand)

def bxl(operand):
    registers["B"] = registers.get("B") ^ operand

def bst(operand):
    registers["B"] = combo_operands(operand) % 8

def jnz(operand):
    global instruction_pointer
    if registers.get("A") != 0:
        instruction_pointer = operand
        return True
    return False

def bxc(operand):
    registers["B"] = registers["B"] ^ registers["C"]

def out(operand):
    return combo_operands(operand) % 8

def bdv(operand):
    registers["B"] = registers.get("A") // 2 ** combo_operands(operand)

def cdv(operand):
    registers["C"] = registers.get("A") // 2 ** combo_operands(operand)

opcode_dict = {0: adv, 1: bxl, 2:bst, 3:jnz, 4:bxc, 5:out, 6:bdv, 7:cdv}
output = []
instruction_pointer = 0

while instruction_pointer < len(instructions)-1:
    opcode, operand = instructions[instruction_pointer], instructions[instruction_pointer+1]
    current_function = opcode_dict.get(opcode)
    current_output = current_function(operand)

    if is_strict_int(current_output):
        output.append(current_output)

    if opcode != 3 or current_output != True:
        instruction_pointer += 2

print(output)

# Task 2
register_A_value = 8**14 # 8**15 should be the max possible value
"""
while output != instructions:
    if register_A_value % 1000000 == 0:
        print(register_A_value)
    register_A_value += 1
    output = []
    instruction_pointer = 0
    registers["A"] = register_A_value
    while instruction_pointer < len(instructions) - 1:
        opcode, operand = instructions[instruction_pointer], instructions[instruction_pointer + 1]
        current_function = opcode_dict.get(opcode)
        current_output = current_function(operand)

        if is_strict_int(current_output):
            output.append(current_output)
            if output != instructions[:len(output)]:
                break

        if opcode != 3 or current_output != True:
            instruction_pointer += 2

print(register_A_value)

"""
def check_equation(result, A):
    #(((A % 8) XOR 1) XOR 5) XOR (A // 2 ^ ((A % 8) XOR 1)) % 8
    x1 = ((A%8) ^ 1) ^ 5
    x2 = (A // 2) ** ((A%8)^1)

    return result == (x1 ^ x2) % 8

def verify_instructions(A):
    for instruction in instructions:
        if not check_equation(instruction, A):
            return False
        A = A // 8
    return True

for A in range(8**14, 8**15):
    if A % 10**6 == 0:
        print(A)
    if verify_instructions(A):
        print(A)
        break

# What happens in the first go:
# 1: B = A % 8
# 2: B = B XOR 1
# 3: C = A // 2^(B)
# 4: B = B XOR 5
# 5: B = B XOR C
# 6: 2 = B % 8
# 7: A = A // 8

# We can find the possible range of A using the last condition
# A // 8^14 > 0
# A // 8^15 = 0

# 8^14 < A < 8^15


# Let's try to solve the equation above
# B = (A%8) XOR 1
# C = A // 2^((A%8) XOR 1)
# B = ((A%8) XOR 1) XOR 5
# B = (((A%8) XOR 1) XOR 5) XOR (A // 2^((A%8) XOR 1))
# 2 = (((A%8) XOR 1) XOR 5) XOR (A // 2^((A%8) XOR 1)) % 8
# 8k + 2 = ((A%8) XOR 1) XOR 5) XOR (A // 2^((A%8) XOR 1)