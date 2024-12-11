# Import necessary modules
from collections import Counter
from typing import Counter as CounterType

def transform_stones_with_count(stones: CounterType[int]) -> CounterType[int]:
    """
    Transform the stones according to the rules, using a frequency count to optimize.

    Parameters:
        stones (CounterType[int]): A Counter mapping each stone value to its frequency.

    Returns:
        CounterType[int]: A new Counter with transformed stones and their frequencies.
    """
    new_stones = Counter()
    for stone, count in stones.items():
        if stone == 0:
            # Rule 1: Replace 0 with 1
            new_stones[1] += count
        elif len(str(stone)) % 2 == 0:
            # Rule 2: Split stones with an even number of digits
            digits = str(stone)
            half = len(digits) // 2
            left, right = int(digits[:half]), int(digits[half:])
            new_stones[left] += count
            new_stones[right] += count
        else:
            # Rule 3: Multiply by 2024
            new_stones[stone * 2024] += count
    return new_stones

def simulate_blinks(file_path: str, blinks: int) -> int:
    """
    Simulate the blinking process for a given number of iterations, using frequency counts.

    Parameters:
        file_path (str): Path to the input file containing the initial stone arrangement.
        blinks (int): The number of times to blink.

    Returns:
        int: The number of stones after the specified number of blinks.
    """
    # Read the initial arrangement from the file
    with open(file_path, 'r') as file:
        initial_stones = map(int, file.read().strip().split())

    # Initialize a Counter to track stone frequencies
    stone_counter = Counter(initial_stones)

    # Perform the transformations for the given number of blinks
    for _ in range(blinks):
        stone_counter = transform_stones_with_count(stone_counter)

    # Return the total count of stones
    return sum(stone_counter.values())

# Example usage
if __name__ == "__main__":
    # Specify the input file and number of blinks
    input_file = "input.txt"
    num_blinks = 25
    num_blinks2 = 75

    # Run the simulation
    result = simulate_blinks(input_file, num_blinks)
    result2 = simulate_blinks(input_file, num_blinks2)

    # Output the result
    print(f"Number of stones after {num_blinks} blinks: {result}")
    print(f"Number of stones after {num_blinks2} blinks: {result2}")
