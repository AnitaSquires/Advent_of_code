# Open the input file and read the contents
with open('input.txt', 'r') as file:
    puzzle_input = file.readlines()  # Read all lines from the file

# Remove any leading/trailing whitespace characters (such as newlines)
puzzle_input = [line.strip() for line in puzzle_input]


def is_safe_report(report):
    # Check if the levels are either increasing or decreasing
    increasing = True
    decreasing = True

    for i in range(1, len(report)):
        diff = abs(report[i] - report[i - 1])

        # The difference between adjacent levels must be at least 1 and at most 3
        if diff < 1 or diff > 3:
            return False

        # Check if the report is increasing or decreasing
        if report[i] <= report[i - 1]:
            increasing = False
        if report[i] >= report[i - 1]:
            decreasing = False

    # Report is safe if it's either increasing or decreasing
    return increasing or decreasing


def is_safe_with_one_removal(report):
    # Try removing each level one by one and check if it becomes safe
    for i in range(len(report)):
        new_report = report[:i] + report[i + 1:]  # Remove the i-th level
        if is_safe_report(new_report):
            return True
    return False


def count_safe_reports(reports, allow_removal=False):
    safe_count = 0

    for report in reports:
        # First check if the report is safe
        if is_safe_report(report):
            safe_count += 1
        # If the report is not safe, and removal is allowed, check if removing one level makes it safe
        elif allow_removal and is_safe_with_one_removal(report):
            safe_count += 1

    return safe_count


# Example input data (the given puzzle input)
data = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9"
]

# Parse the input and convert each report into a list of integers
report_01 = [list(map(int, report.split())) for report in data]
reports_02 = [list(map(int, report.split())) for report in puzzle_input]

# Part 1: Count the number of safe reports without the Problem Dampener
safe_reports_count_part_test_1 = count_safe_reports(report_01, allow_removal=False)
safe_reports_count_part1 = count_safe_reports(reports_02, allow_removal=False)
print(f"Part 1 - Safe reports without removal test: {safe_reports_count_part_test_1}")
print(f"Part 1 - Safe reports without removal: {safe_reports_count_part1}")

# Part 2: Count the number of safe reports with the Problem Dampener (allowing one removal)
safe_reports_count_part_test_2 = count_safe_reports(report_01, allow_removal=True)
safe_reports_count_part2 = count_safe_reports(reports_02, allow_removal=True)
print(f"Part 2 - Safe reports without removal test: {safe_reports_count_part_test_2}")
print(f"Part 2 - Safe reports with removal: {safe_reports_count_part2}")
