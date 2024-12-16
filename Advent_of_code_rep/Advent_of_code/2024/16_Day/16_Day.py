import heapq  # Import the heapq module for using a priority queue (min-heap) to facilitate Dijkstra's algorithm


# Function to parse input and create a grid and starting/ending points
def parse(lines):
    grid = []  # Initialize an empty grid to store the map
    line = 0  # This variable seems to be unnecessary since `line` is re-assigned in the loop, you can ignore it.
    for line in range(len(lines)):  # Loop through each line in the input data
        grid.append(list(lines[line].strip()))  # Convert each line to a list of characters and add it to the grid

    s = None  # Initialize starting point variable
    e = None  # Initialize ending point variable
    for r, row in enumerate(grid):  # Iterate over each row in the grid
        for c, ch in enumerate(row):  # Iterate over each character in the row
            if ch == "S":  # If the character is 'S', it represents the start point
                s = (r, c)  # Store the row and column indices of the start point
            elif ch == "E":  # If the character is 'E', it represents the end point
                e = (r, c)  # Store the row and column indices of the end point
    return grid, s, e  # Return the grid, start position, and end position


# Dijkstra's algorithm for finding the shortest path on the grid
def dijkstra(grid, starts):
    # delta defines the movement direction deltas for 'E', 'W', 'N', 'S' (East, West, North, South)
    delta = {"E": (0, 1), "W": (0, -1), "N": (-1, 0), "S": (1, 0)}

    dist = {}  # Dictionary to store the shortest distance for each (row, col, direction)
    pq = []  # Min-heap priority queue to select the next node to process

    # Initialize the starting positions in the priority queue with distance 0
    for sr, sc, dir in starts:
        dist[(sr, sc, dir)] = 0  # Set the initial distance to 0
        heapq.heappush(pq, (0, sr, sc, dir))  # Push the starting position into the priority queue

    # Dijkstra's algorithm loop
    while pq:
        (d, row, col, direction) = heapq.heappop(pq)  # Pop the element with the smallest distance (d)
        if dist[(row, col, direction)] < d:  # If the current distance is greater than a previously found one, skip it
            continue

        # For each direction, except the current direction, add to the priority queue if it leads to a better distance
        for next_dir in "EWNS".replace(direction, ""):  # Iterate over other directions (excluding current direction)
            if (row, col, next_dir) not in dist or dist[
                (row, col, next_dir)] > d + 1000:  # Check if the direction needs updating
                dist[(row, col, next_dir)] = d + 1000  # Update the distance to the new direction
                heapq.heappush(pq, (d + 1000, row, col, next_dir))  # Push the new state to the priority queue

        # Calculate the next row and column based on the direction
        dr, dc = delta[direction]  # Get the row and column deltas for the direction
        next_row, next_col = row + dr, col + dc  # Calculate the next row and column

        # Check if the next position is within bounds, not a wall ('#'), and the distance is better
        if (
                0 <= next_row < len(grid)  # Check row bounds
                and 0 <= next_col < len(grid[0])  # Check column bounds
                and grid[next_row][next_col] != "#"  # Ensure it's not a wall
                and (
                (next_row, next_col, direction) not in dist  # If the position hasn't been visited
                or dist[(next_row, next_col, direction)] > d + 1  # Or if the new distance is better
        )
        ):
            dist[(next_row, next_col, direction)] = d + 1  # Update the distance for the new position
            heapq.heappush(pq, (d + 1, next_row, next_col, direction))  # Push the new state to the priority queue

    return dist  # Return the dictionary containing the shortest distance for each (row, col, direction)


# Part 1: Function to calculate the shortest path distance from start to end
def part1(input):
    grid, (sr, sc), (er, ec) = input  # Unpack the input: grid, start and end positions
    dist = dijkstra(grid, [(sr, sc, "E")])  # Call Dijkstra with the start position and initial direction "E" (East)
    best = 1000000000  # Initialize the best (shortest) distance to a large number
    for dir in "EWNS":  # Iterate over all possible directions (East, West, North, South)
        if (er, ec, dir) in dist:  # Check if the end position has a valid distance for this direction
            best = min(best, dist[(er, ec, dir)])  # Update the best distance to the minimum found
    return best  # Return the shortest path distance


# Part 2: Function to calculate the optimal solution by considering paths from both start and end
def part2(input):
    grid, (sr, sc), (er, ec) = input  # Unpack the input: grid, start and end positions
    from_start = dijkstra(grid, [(sr, sc, "E")])  # Get distances from the start
    from_end = dijkstra(grid, [(er, ec, d) for d in "EWNS"])  # Get distances from the end for all directions
    optimal = part1(input)  # Get the optimal (shortest) distance from part1
    flip = {"E": "W", "W": "E", "N": "S", "S": "N"}  # Flip directions (East <-> West, North <-> South)
    result = set()  # Initialize a set to store valid positions

    # Loop through each position in the grid
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            for dir in "EWNS":  # For each direction
                state_from_start = (row, col, dir)  # State from the start point
                state_from_end = (row, col, flip[dir])  # State from the end point (with flipped direction)
                if state_from_start in from_start and state_from_end in from_end:  # Check if both directions are valid
                    if (
                            from_start[state_from_start] + from_end[state_from_end]  # Total distance from start and end
                            == optimal  # If the sum equals the optimal distance, add the position to the result
                    ):
                        result.add((row, col))  # Add the position to the result set
    return len(result)  # Return the number of valid positions


# Parse sample and real input files
sample = parse(open("test.txt").readlines())  # Read and parse the test input file
real = parse(open("input.txt").readlines())  # Read and parse the real input file
input = real  # Use the real input for processing

# Print the results for both parts of the task
print(part1(input))  # Output the result for part 1
print(part2(input))  # Output the result for part 2
