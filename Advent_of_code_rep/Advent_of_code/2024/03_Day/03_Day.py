import re

# Open and read the input file
with open("input.txt") as f:
    # Read the file content, strip any leading/trailing whitespace
    data = f.read().strip()

# PART 1: Calculate the total sum of all mul(X, Y) instructions in the data
# Find all instances of "mul(X, Y)" using regex, where X and Y are numbers
# Multiply each pair and calculate their total sum
result_1 = sum(int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", data))

# Print the result of Part 1
print("Solution 1:", result_1)

# PART 2: Process data to respect "do()" and "don't()" instructions
# Initialize the total result for Part 2
result_2 = 0

# Split the input data into sections based on the "do()" instructions
do_muls = data.split("do()")

# Process each "do()" section individually
for do_mul in do_muls:
    # For each section, split by "don't()" and take the first part
    # Only the portion before "don't()" is valid for multiplication
    do = do_mul.split("don't()")[0]

    # Extract all "mul(X, Y)" pairs in the valid section and calculate their sum
    result_2 += sum(int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", do))

# Print the result of Part 2
print("Solution 2:", result_2)