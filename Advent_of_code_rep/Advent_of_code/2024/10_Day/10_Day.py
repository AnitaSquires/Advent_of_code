from collections import deque


def read_input():
    """
    Reads the input file `input.txt` and parses it into a 2D list of integers.

    Returns:
        list[list[int]]: A grid representing the topographic map, where each integer
        represents the height at that position.
    """
    with open('input.txt', 'r') as file:
        return [[int(x) for x in line.strip()] for line in file]


def get_neighbors(x, y, grid):
    """
    Computes the valid neighbors of a given position (x, y) in the grid.

    Args:
        x (int): The x-coordinate of the current position.
        y (int): The y-coordinate of the current position.
        grid (list[list[int]]): The topographic grid.

    Returns:
        list[tuple[int, int]]: A list of (x, y) tuples representing valid neighboring positions.
    """
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    neighbors = []
    height = len(grid)
    width = len(grid[0])

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < height and 0 <= new_y < width:
            neighbors.append((new_x, new_y))

    return neighbors


def count_paths(start_x, start_y, grid):
    """
    Counts all valid paths from a trailhead (height 0) to height 9,
    where each step must increase in height by exactly 1.

    Args:
        start_x (int): The x-coordinate of the trailhead.
        start_y (int): The y-coordinate of the trailhead.
        grid (list[list[int]]): The topographic grid.

    Returns:
        int: The number of valid paths from the trailhead to a 9.
    """
    memo = {}  # Memoization to avoid redundant calculations

    def dfs(x, y, current_height):
        """
        Depth-First Search helper to recursively count paths.

        Args:
            x (int): Current x-coordinate.
            y (int): Current y-coordinate.
            current_height (int): Current height in the path.

        Returns:
            int: Total paths from this position to a height of 9.
        """
        if (x, y, current_height) in memo:
            return memo[(x, y, current_height)]

        if grid[x][y] == 9:  # Reached a height of 9
            return 1

        total_paths = 0

        for next_x, next_y in get_neighbors(x, y, grid):
            next_height = grid[next_x][next_y]
            if next_height == current_height + 1:
                total_paths += dfs(next_x, next_y, next_height)

        memo[(x, y, current_height)] = total_paths
        return total_paths

    return dfs(start_x, start_y, 0)


def find_trailheads(grid):
    """
    Identifies all trailheads (positions with height 0) in the grid.

    Args:
        grid (list[list[int]]): The topographic grid.

    Returns:
        list[tuple[int, int]]: A list of (x, y) coordinates of trailheads.
    """
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def find_reachable_nines(start_x, start_y, grid):
    """
    Finds all reachable positions with height 9 from a trailhead (start_x, start_y).

    Args:
        start_x (int): The x-coordinate of the trailhead.
        start_y (int): The y-coordinate of the trailhead.
        grid (list[list[int]]): The topographic grid.

    Returns:
        set[tuple[int, int]]: A set of coordinates representing all reachable height-9 positions.
    """
    visited, reachable_nines = set(), set()
    queue = deque([(start_x, start_y, 0)])  # Queue stores (x, y, current height)

    while queue:
        x, y, current_height = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if grid[x][y] == 9:
            reachable_nines.add((x, y))
            continue

        for next_x, next_y in get_neighbors(x, y, grid):
            next_height = grid[next_x][next_y]

            if next_height == current_height + 1:
                queue.append((next_x, next_y, next_height))

    return reachable_nines


def first_part(grid):
    """
    Calculates the total score for the first part, which is the sum of all reachable
    height-9 positions from every trailhead.

    Args:
        grid (list[list[int]]): The topographic grid.

    Returns:
        int: Total score for the first part.
    """
    total_score = 0
    trailheads = find_trailheads(grid)

    for x, y in trailheads:
        reachable_nines = find_reachable_nines(start_x=x, start_y=y, grid=grid)
        score = len(reachable_nines)
        total_score += score

    return total_score


def second_part(grid):
    """
    Calculates the total score for the second part, which is the total number
    of valid paths from all trailheads to height-9 positions.

    Args:
        grid (list[list[int]]): The topographic grid.

    Returns:
        int: Total score for the second part.
    """
    total = 0
    trailheads = find_trailheads(grid)

    for x, y in trailheads:
        rating = count_paths(x, y, grid)
        total += rating

    return total


if __name__ == "__main__":
    grid = read_input()

    # First part: Sum of reachable height-9 positions
    print("First part result: " + str(first_part(grid)))

    # Second part: Total number of valid paths to height-9 positions
    print("Second part result: " + str(second_part(grid)))
