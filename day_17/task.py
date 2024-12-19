from pathlib import Path

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

def combo_operands(number):
    if number < 4:
        return number
    else:
        return registers.get(chr(ord("A")+ (number%4)))

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

    if opcode == 5:
        output.append(current_output)

    if opcode != 3 or current_output != True:
        instruction_pointer += 2

print(output)

# Task 2

# What happens in the first go:
# 1: B = A % 8
# 2: B = B XOR 1
# 3: C = A // 2^(B)
# 4: B = B XOR 5
# 5: B = B XOR C
# 6: 2 = B % 8
# 7: A = A // 8

# Let's try to solve the equation above
# B = (A%8) XOR 1
# C = A // 2^((A%8) XOR 1)
# B = ((A%8) XOR 1) XOR 5
# B = (((A%8) XOR 1) XOR 5) XOR (A // 2^((A%8) XOR 1))
# 2 = (((A%8) XOR 1) XOR 5) XOR (A // 2^((A%8) XOR 1)) % 8
# 010 = (((A%8) XOR 1) XOR 5) XOR (A // 2^((A%8) XOR 1)) % 8
# 0b010 = (((A & 0b111) XOR 0b001) XOR 0b101) XOR (A >> (A & (0b111) XOR 0b001)) & 0b111
# 0b010 = ((A & 0b111) XOR 0b100) XOR(A >> (A & (0b111) XOR 0b001))) & 0b111

# We solve this for all the instructions, starting with the last ones,
# So we can guarantee that we find the lowest possible answer


def get_msb(number, msb_count=3):
    if number.bit_length() <= msb_count:
        return number
    return number >> (number.bit_length() - msb_count)

def get_lsb(number, n_bits):
    mask = (1 << n_bits) - 1
    return number & mask

def check_instructions(result, A):
    lsb3 = A & 0b111
    t1 = (lsb3 ^ 0b001) ^ 0b101
    t2 = lsb3 ^ 0b001
    t3 = (A >> t2)
    return (t1 ^ t3) & 0b111 == result

def solve_A(current_step, current_number):
    if current_step == len(instructions):
        return current_number

    solution = instructions[-1 - current_step]
    for addition in range(0b1000):
        A = (current_number << 3) | addition
        if check_instructions(solution, A):
            answer = solve_A(current_step + 1, A)
            if answer is not None:
                return answer
    return None

register_a = solve_A(0, 0b0)
print(register_a)