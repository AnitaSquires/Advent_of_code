def extract_calibration_value(line):
    # Extract the first and last digit from the line
    first_digit = None
    last_digit = None

    # Iterate over the characters in the line
    for char in line:
        if char.isdigit():
            if first_digit is None:
                first_digit = char  # First digit found
            last_digit = char  # Always update last digit

    # Combine the first and last digit to form the two-digit number
    return int(first_digit + last_digit)


def sum_of_calibration_values(file_path):
    total = 0
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove any surrounding whitespace or newlines
            total += extract_calibration_value(line)
    return total


# Path to the input file
file_path = 'input'

# Calculate the result
result = sum_of_calibration_values(file_path)
print(result)