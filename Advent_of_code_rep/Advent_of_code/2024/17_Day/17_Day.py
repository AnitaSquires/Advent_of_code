import sys
from typing import List

# Specify the input file via command-line argument or use "input.txt" as default
FILE = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def read_lines_to_list() -> List[str]:
    """
    Reads lines from the input file, strips whitespace, and returns them as a list of strings.

    Returns:
        List[str]: The lines of the input file as a list of strings.
    """
    lines: List[str] = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # Remove leading and trailing whitespace
            lines.append(line)

    return lines

def combo(register_a, register_b, register_c, operand) -> int:
    """
    Computes the value associated with the operand based on the combo rules.

    Args:
        register_a (int): The value of register A.
        register_b (int): The value of register B.
        register_c (int): The value of register C.
        operand (int): The operand to evaluate.

    Returns:
        int: The evaluated operand value.
    """
    if operand in [0, 1, 2, 3]:  # Literal values
        combo = operand
    elif operand == 4:  # Value from register A
        combo = register_a
    elif operand == 5:  # Value from register B
        combo = register_b
    elif operand == 6:  # Value from register C
        combo = register_c
    elif operand == 7:  # Reserved operand value (invalid in this context)
        raise Exception("this is a reserved combo operand")
    else:  # Invalid operand
        raise Exception("you messed up")

    return combo

def part_one():
    """
    Executes the program in part one and calculates the output sequence.
    """
    lines = read_lines_to_list()  # Read the input
    answer = ""

    # Parse registers and program instructions from the input
    register_a = int(lines[0].split(": ")[-1])  # Extract initial value of register A
    register_b = int(lines[1].split(": ")[-1])  # Extract initial value of register B
    register_c = int(lines[2].split(": ")[-1])  # Extract initial value of register C
    program = [int(v) for v in lines[4].split(": ")[-1].split(",")]  # Parse the program into a list of integers

    pc = 0  # Program counter
    out = []  # Output values

    # Process instructions until the program counter exceeds program length
    while pc < len(program):
        opcode = program[pc]  # Current instruction opcode
        operand = program[pc + 1]  # Operand for the current instruction
        combo_operand = combo(register_a, register_b, register_c, operand)  # Evaluate operand

        # Execute the instruction based on the opcode
        if opcode == 0:
            # adv: Perform integer division on register A
            register_a = register_a // pow(2, combo_operand)
        elif opcode == 1:
            # bxl: Bitwise XOR of register B with the operand
            register_b = register_b ^ operand
        elif opcode == 2:
            # bst: Store (combo operand % 8) in register B
            register_b = combo_operand % 8
        elif opcode == 3:
            # jnz: Jump to the operand if register A is non-zero
            if register_a != 0:
                pc = operand
                continue  # Skip incrementing the program counter
        elif opcode == 4:
            # bxc: Bitwise XOR of register B with register C
            register_b = register_b ^ register_c
        elif opcode == 5:
            # out: Append (combo operand % 8) to the output
            out.append(f"{combo_operand % 8}")
        elif opcode == 6:
            # bdv: Integer division of register A, store result in register B
            register_b = register_a // pow(2, combo_operand)
        elif opcode == 7:
            # cdv: Integer division of register A, store result in register C
            register_c = register_a // pow(2, combo_operand)
        else:
            # Invalid opcode
            raise Exception("non-existent opcode!")

        pc += 2  # Move to the next instruction (each instruction is 2 units long)

    # Join the output values into a comma-separated string
    answer = ",".join(out)
    print(f"Part 1: {answer}")

def part_two():
    """
    Solves part two by finding the smallest initial value of register A
    that causes the program to output a copy of itself.
    """
    lines = read_lines_to_list()  # Read the input
    answer = 0

    # Parse the program instructions
    program = [int(v) for v in lines[4].split(": ")[-1].split(",")]

    def test(a):
        """
        Calculate the output of the program based on a test value for register A.

        Args:
            a (int): The test value for register A.

        Returns:
            int: The result of the program's computation based on register A.
        """
        return (((a % 8) ^ 1) ^ 5) ^ (a // pow(2, ((a % 8) ^ 1))) % 8

    answers = [0]  # Initialize with a possible answer
    for p in reversed(program):  # Iterate through the program in reverse
        new_answers = []  # Store potential answers for the current program step
        for curr in answers:  # For each current possible output
            for a in range(8):  # Test all values for a single 3-bit operand
                to_test = (curr << 3) + a  # Calculate a potential value for register A
                out = test(to_test)  # Compute the output
                if out == p:  # If the output matches the program
                    new_answers.append(to_test)  # Add to the list of potential answers

        answers = new_answers  # Update the list of potential answers

    answer = min(answers)  # Find the smallest valid initial value for register A

    print(f"Part 2: {answer}")

# Execute both parts
part_one()
part_two()
