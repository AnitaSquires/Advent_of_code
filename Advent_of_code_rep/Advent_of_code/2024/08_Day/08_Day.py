from collections import defaultdict


def get_antennas(grid):
    """
    Parse the grid to find all antennas.

    Args:
        grid (list of str): A list of strings representing the grid.

    Returns:
        dict: A dictionary where the keys are antenna identifiers (e.g., 'A', 'B', etc.),
              and the values are lists of (row, col) coordinates of each antenna's location.
    """
    antennas = defaultdict(list)

    for row, line in enumerate(grid):  # Iterate over each row in the grid
        for col, char in enumerate(line):  # Iterate over each character in the row
            if char != ".":  # If the character is not '.', it's an antenna
                antennas[char].append((row, col))

    return antennas


def on_grid(node, n_rows, n_cols):
    """
    Check if a given coordinate is within the bounds of the grid.

    Args:
        node (tuple): A tuple (row, col) representing the position to check.
        n_rows (int): Total number of rows in the grid.
        n_cols (int): Total number of columns in the grid.

    Returns:
        bool: True if the node is within bounds, False otherwise.
    """
    return 0 <= node[0] < n_rows and 0 <= node[1] < n_cols


def main():
    """
    Main function to compute the number of unique antinodes based on a given grid.

    Part 1:
        - Identify antinodes (potential connections) that are reachable by moving in the
          reverse direction from an antenna pair until out of bounds.

    Part 2:
        - Additionally identify all intermediate antinodes that can be visited along the
          path from one antenna to another.
    """
    # Read the grid from input.txt
    with open("input.txt", "rt") as f:
        grid = [line.strip() for line in f]  # Strip whitespace and read lines into a list
        n_rows, n_cols = len(grid), len(grid[0])  # Get grid dimensions

    # Get the coordinates of all antennas grouped by their identifiers
    antennas = get_antennas(grid)

    # Sets to track antinodes for Part 1 and Part 2
    antinodes_part1 = set()
    antinodes_part2 = set()

    # Iterate over each group of antenna locations
    for locations in antennas.values():
        if len(locations) == 1:  # Skip antennas with only one location
            continue

        # Compare every pair of antenna locations in the group
        for i1 in range(len(locations) - 1):
            loc1 = locations[i1]  # First antenna location

            for i2 in range(i1 + 1, len(locations)):
                loc2 = locations[i2]  # Second antenna location
                row_diff, coll_diff = loc2[0] - loc1[0], loc2[1] - loc1[1]  # Difference vector

                # Add both locations to Part 2 (they are always part of the path)
                antinodes_part2.add(loc1)
                antinodes_part2.add(loc2)

                # Move backward from loc1 in the opposite direction of the difference vector
                antinode = (loc1[0] - row_diff, loc1[1] - coll_diff)
                if on_grid(antinode, n_rows, n_cols):  # Ensure it's within grid bounds
                    antinodes_part1.add(antinode)  # Add to Part 1
                    # Continue moving backward until out of bounds
                    while on_grid(
                            antinode := (antinode[0] - row_diff, antinode[1] - coll_diff),
                            n_rows,
                            n_cols,
                    ):
                        antinodes_part2.add(antinode)  # Add to Part 2

                # Move forward from loc2 in the direction of the difference vector
                antinode = (loc2[0] + row_diff, loc2[1] + coll_diff)
                if on_grid(antinode, n_rows, n_cols):  # Ensure it's within grid bounds
                    antinodes_part1.add(antinode)  # Add to Part 1
                    # Continue moving forward until out of bounds
                    while on_grid(
                            antinode := (antinode[0] + row_diff, antinode[1] + coll_diff),
                            n_rows,
                            n_cols,
                    ):
                        antinodes_part2.add(antinode)  # Add to Part 2

    # Output results
    print(f"Part 1: {len(antinodes_part1)}")  # Unique antinodes for Part 1
    print(f"Part 2: {len(antinodes_part1 | antinodes_part2)}")  # Union of both sets


if __name__ == "__main__":
    main()
