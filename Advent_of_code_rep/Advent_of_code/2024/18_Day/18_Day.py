from bisect import bisect_left  # Import bisect_left for binary search functionality

# Read and parse the input data
# - Reads the file "input.txt"
# - Splits the content into lines, then splits each line by commas
# - Converts each number to an integer and stores the result as a list of tuples
data = open("input.txt").read()
data = [tuple(int(n) for n in line.split(",")) for line in data.split("\n")]

# Define the four cardinal directions for movement:
# - (1, 0): Move down
# - (0, 1): Move right
# - (-1, 0): Move up
# - (0, -1): Move left
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Define a BFS function to find the shortest path from (0, 0) to (W, W)
def bfs(delay=1024, W=70):
    # Set of blocked cells determined by the first 'delay' entries in data
    blocks = set(data[:delay])

    # Initialize the BFS with the starting point (0, 0) and the target point (W, W)
    boundary, target = set([(0, 0)]), (W, W)

    # Track the number of steps and keep a set of seen cells to avoid revisits
    step, seen = 0, set()

    # Perform BFS until there are no more cells to explore
    while boundary:
        newb = set()  # Temporary set for the next layer of cells to explore
        while boundary:
            y, x = boundary.pop()  # Pop a cell from the current boundary
            if (y, x) in seen:  # Skip if already visited
                continue
            if (y, x) == target:  # Return the step count if the target is reached
                return step
            seen.add((y, x))  # Mark the current cell as visited

            # Explore all neighboring cells based on the directions in DIRS
            for dy, dx in DIRS:
                ny, nx = y + dy, x + dx  # Calculate the new coordinates
                # Add valid neighbors (inside bounds and not blocked) to the next layer
                if 0 <= y <= W and 0 <= x <= W and (y, x) not in blocks:
                    newb.add((ny, nx))
        boundary = newb  # Move to the next layer of cells
        step += 1  # Increment the step counter

    # If the target is not reachable, return 0
    return 0

# Call the BFS function with default parameters and print the result
# - Finds the number of steps to reach (70, 70) from (0, 0)
print(bfs())

# Use binary search to find the maximum delay where BFS fails (returns 0)
# - Iterates through data indices
# - Calls bfs() for each delay to determine when the target becomes unreachable
# - Finds the first index where bfs(i) == 0 using bisect_left
# - Outputs the last successful coordinate before BFS fails
print(
    *data[
        bisect_left(
            range(len(data)),  # Range of indices to search
            True,  # Condition to check
            key=lambda i: bfs(i) == 0  # Key function to evaluate bfs(i)
        ) - 1  # Step back to the last successful delay
    ], sep=","
)
