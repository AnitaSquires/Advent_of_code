from itertools import product


def parse_equation(equation):
    """Parse a single equation into the target value and a list of numbers."""
    target, numbers = equation.split(":")
    return int(target), list(map(int, numbers.strip().split()))


def evaluate_left_to_right_basic(numbers, operators):
    """Evaluate a sequence of numbers with the given operators (left-to-right) using only + and *."""
    result = numbers[0]
    for num, op in zip(numbers[1:], operators):
        if op == "+":
            result += num
        elif op == "*":
            result *= num
    return result


def is_solvable_basic(target, numbers):
    """Check if a target value can be achieved using only + and * operators."""
    num_operators = len(numbers) - 1
    for operators in product("+*", repeat=num_operators):
        if evaluate_left_to_right_basic(numbers, operators) == target:
            return True
    return False


def concatenate(a, b):
    """Concatenate two numbers."""
    return int(str(a) + str(b))


def evaluate_with_operators(numbers, operators):
    """Evaluate a sequence of numbers with given operators (left-to-right)."""
    result = numbers[0]
    for num, op in zip(numbers[1:], operators):
        if op == "+":
            result += num
        elif op == "*":
            result *= num
        elif op == "||":
            result = concatenate(result, num)
    return result


def is_solvable_extended(target, numbers):
    """
    Check if a target value can be achieved using +, *, and || operators.
    Tries all possible operator combinations left-to-right.
    """
    num_operators = len(numbers) - 1
    operators_to_try = ['+', '*', '||']

    for operators in product(operators_to_try, repeat=num_operators):
        if evaluate_with_operators(numbers, operators) == target:
            return True
    return False


# Read the input equations from a file
input_file = "input.txt"
with open(input_file, "r") as file:
    equations = file.readlines()

# Compute the total calibration results for both methods
total_calibration_result_basic = 0
total_calibration_result_extended = 0

for equation in equations:
    target, numbers = parse_equation(equation.strip())

    # Check with basic operators (+, *)
    if is_solvable_basic(target, numbers):
        total_calibration_result_basic += target

    # Check with extended operators (+, *, ||)
    if is_solvable_extended(target, numbers):
        total_calibration_result_extended += target

print(f"Total calibration result (basic operators): {total_calibration_result_basic}")
print(f"Total calibration result (extended operators): {total_calibration_result_extended}")
