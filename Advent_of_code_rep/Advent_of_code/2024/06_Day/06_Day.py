def parse_input(input_file):
    """
    Parses the input file to extract the grid, guard's starting position, and direction.

    Args:
        input_file (str): Path to the input file.

    Returns:
        tuple: A tuple containing the grid (list of lists),
               guard's starting position (tuple of x, y),
               and the direction the guard is facing (str).
    """
    with open(input_file, 'r') as file:
        lines = file.read().splitlines()

    grid = [list(line) for line in lines]
    guard_position = None
    direction = None

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in "^v<>":
                guard_position = (x, y)
                direction = char
                grid[y][x] = '.'  # Replace the guard's starting position with an empty space
                break
        if guard_position:
            break

    return grid, guard_position, direction


def turn_right(direction):
    """
    Determines the new direction after a 90-degree right turn.

    Args:
        direction (str): Current direction ('^', 'v', '<', '>').

    Returns:
        str: New direction after the turn.
    """
    return {
        '^': '>',
        '>': 'v',
        'v': '<',
        '<': '^',
    }[direction]


def move_forward(position, direction):
    """
    Calculates the new position after moving one step forward.

    Args:
        position (tuple): Current position as (x, y).
        direction (str): Current direction ('^', 'v', '<', '>').

    Returns:
        tuple: New position as (x, y).
    """
    x, y = position
    if direction == '^':
        return (x, y - 1)
    elif direction == 'v':
        return (x, y + 1)
    elif direction == '<':
        return (x - 1, y)
    elif direction == '>':
        return (x + 1, y)


def simulate_guard(grid, guard_position, direction, obstruction=None):
    """
    Simulates the guard's movement and determines the visited positions.

    Args:
        grid (list of list of str): The map of the lab.
        guard_position (tuple): Guard's starting position as (x, y).
        direction (str): Guard's initial direction.
        obstruction (tuple, optional): Position of a new obstruction to temporarily place. Defaults to None.

    Returns:
        tuple: A set of visited positions and a boolean indicating if a loop was detected.
    """
    visited_positions = set()
    path_history = set()
    current_position = guard_position
    current_direction = direction

    # Temporarily place the obstruction if provided
    if obstruction:
        x, y = obstruction
        grid[y][x] = '#'

    while True:
        visited_positions.add(current_position)
        state = (current_position, current_direction)

        if state in path_history:
            # Loop detected
            if obstruction:
                grid[obstruction[1]][obstruction[0]] = '.'
            return visited_positions, True
        path_history.add(state)

        next_position = move_forward(current_position, current_direction)
        x, y = next_position

        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            # Guard left the map
            break

        if grid[y][x] == '#':
            current_direction = turn_right(current_direction)
        else:
            current_position = next_position

    # Remove obstruction if it was placed
    if obstruction:
        grid[obstruction[1]][obstruction[0]] = '.'

    return visited_positions, False


def part_one(input_file):
    """
    Solves Part 1 by predicting the guard's patrol path and counting distinct visited positions.

    Args:
        input_file (str): Path to the input file.

    Returns:
        int: The number of distinct positions visited by the guard.
    """
    grid, guard_position, direction = parse_input(input_file)
    visited_positions, _ = simulate_guard(grid, guard_position, direction)
    return len(visited_positions)


def part_two(input_file):
    """
    Solves Part 2 by finding the number of positions where adding an obstruction causes a loop.

    Args:
        input_file (str): Path to the input file.

    Returns:
        int: The number of positions that can cause the guard to loop.
    """
    grid, guard_position, direction = parse_input(input_file)
    possible_positions = set()

    # Precompute the guard's path without obstructions
    initial_visited, _ = simulate_guard(grid, guard_position, direction)

    for x, y in initial_visited:
        if grid[y][x] == '.' and (x, y) != guard_position:
            # Simulate with obstruction at (x, y)
            _, is_loop = simulate_guard(grid, guard_position, direction, obstruction=(x, y))
            if is_loop:
                possible_positions.add((x, y))

    return len(possible_positions)


# Specify the input file
input_file = "input.txt"

# Solve Part 1
part_one_result = part_one(input_file)
print("Part 1 - Distinct positions visited by the guard:", part_one_result)

# Solve Part 2
part_two_result = part_two(input_file)
print("Part 2 - Positions causing a loop:", part_two_result)
