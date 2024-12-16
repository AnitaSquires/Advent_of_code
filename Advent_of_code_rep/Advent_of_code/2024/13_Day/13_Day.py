from collections import namedtuple
import re

# Read the input file and strip trailing whitespaces from each line
with open('input.txt') as f:
    lines = [line.rstrip() for line in f]

# Define a named tuple to represent each claw machine configuration
Claw = namedtuple('Claw', ['button_a', 'button_b', 'prize'])
claws = []

# Parse the input file in chunks of 4 lines, corresponding to the button configurations and prize positions
for i in range(0, len(lines) // 4 + 1):
    # Extract button A configuration (e.g., "Button A: X+94, Y+34") using regex to find integers
    a = tuple([int(x) for x in re.findall(r'\d+', lines[i * 4])])
    # Extract button B configuration (e.g., "Button B: X+22, Y+67")
    b = tuple([int(x) for x in re.findall(r'\d+', lines[i * 4 + 1])])
    # Extract prize coordinates (e.g., "Prize: X=8400, Y=5400")
    p = tuple([int(x) for x in re.findall(r'\d+', lines[i * 4 + 2])])
    # Add the parsed data as a Claw object to the list of claws
    claws.append(Claw(a, b, p))


# Function to find the minimum token cost to win the prize for a single claw machine
def find_solution(test_claw: Claw, incr=0):
    # Unpack the claw machine's button configurations and prize coordinates
    ax, ay = test_claw.button_a  # Button A moves (ax, ay)
    bx, by = test_claw.button_b  # Button B moves (bx, by)
    px, py = test_claw.prize  # Prize is at position (px, py)

    # Add the increment for Part 2 (this modifies the prize coordinates by a large constant)
    px += incr
    py += incr

    # Initialize solution variables. If no integer solution exists, they remain None
    solution_a, solution_b = None, None

    # Algebraic equation to solve for the number of button presses (A and B)
    # Check if solution for A is an integer by comparing regular and integer division results
    if (bx * py - by * px) / (bx * ay - by * ax) == (bx * py - by * px) // (bx * ay - by * ax):
        # Calculate integer solution for A (number of Button A presses)
        solution_a = (bx * py - by * px) // (bx * ay - by * ax)

        # Check if solution for B is also an integer
        if (py - solution_a * ay) / by == (py - solution_a * ay) // by:
            solution_b = (py - solution_a * ay) // by

    # If both solutions are valid integers, return the total token cost
    if solution_a is not None and solution_b is not None:
        return solution_a * 3 + solution_b  # Button A costs 3 tokens, Button B costs 1 token
    else:
        # Return 0 if no valid solution exists
        return 0


# Initialize total costs for Part 1 and Part 2
total_cost_1 = 0  # Part 1: original prize positions
total_cost_2 = 0  # Part 2: prize positions adjusted by the increment

# The increment for Part 2 modifies prize positions significantly
increase = 10000000000000

# Calculate total costs by iterating over all claw machines
for this_claw in claws:
    # Add the cost for this claw machine in Part 1 (no increment)
    total_cost_1 += find_solution(this_claw)
    # Add the cost for this claw machine in Part 2 (with increment)
    total_cost_2 += find_solution(this_claw, increase)

# Print the results for Part 1 and Part 2
print(f"Part 1: {total_cost_1}")  # Total cost for winning all prizes in Part 1
print(f"Part 2: {total_cost_2}")  # Total cost for winning all prizes in Part 2