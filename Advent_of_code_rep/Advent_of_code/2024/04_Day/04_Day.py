def count_xmas_and_xmas_occurrences(file_path):
    """
    Counts occurrences of the XMAS word and X-MAS pattern in a 2D grid read from a file.

    Args:
    file_path (str): Path to the input file containing the grid.

    Returns:
    tuple: (XMAS count, X-MAS count)
    """
    # Read the grid from the input file
    with open(file_path, 'r') as f:
        grid = [line.strip() for line in f.readlines()]

    rows = len(grid)
    cols = len(grid[0])

    # Count XMAS occurrences
    word = "XMAS"
    word_length = len(word)
    directions = [
        (0, 1),  # Horizontal right
        (0, -1),  # Horizontal left
        (1, 0),  # Vertical down
        (-1, 0),  # Vertical up
        (1, 1),  # Diagonal down-right
        (-1, -1),  # Diagonal up-left
        (1, -1),  # Diagonal down-left
        (-1, 1)  # Diagonal up-right
    ]

    def is_valid_word(x, y, dx, dy):
        """Checks if a word fits starting at (x, y) in the direction (dx, dy)."""
        for i in range(word_length):
            nx, ny = x + i * dx, y + i * dy
            if nx < 0 or ny < 0 or nx >= rows or ny >= cols or grid[nx][ny] != word[i]:
                return False
        return True

    xmas_count = 0
    for row in range(rows):
        for col in range(cols):
            for dx, dy in directions:
                if is_valid_word(row, col, dx, dy):
                    xmas_count += 1

    # Count X-MAS occurrences
    def is_valid_xmas(x, y):
        """Checks if an X-MAS pattern exists centered at (x, y)."""
        # Ensure the 3x3 grid around (x, y) is within bounds
        if x - 1 < 0 or x + 1 >= rows or y - 1 < 0 or y + 1 >= cols:
            return False

        # Check the "X" diagonals and vertical components
        top_left = grid[x - 1][y - 1]
        bottom_right = grid[x + 1][y + 1]
        top_right = grid[x - 1][y + 1]
        bottom_left = grid[x + 1][y - 1]
        center = grid[x][y]

        return (
            # MAS in the top-left to bottom-right diagonal
                (top_left == "M" and center == "A" and bottom_right == "S") or
                (top_left == "S" and center == "A" and bottom_right == "M")
        ) and (
            # MAS in the top-right to bottom-left diagonal
                (top_right == "M" and center == "A" and bottom_left == "S") or
                (top_right == "S" and center == "A" and bottom_left == "M")
        )

    x_mas_count = 0
    for row in range(rows):
        for col in range(cols):
            if is_valid_xmas(row, col):
                x_mas_count += 1

    return xmas_count, x_mas_count


# Specify the path to the input file
file_path = "input.txt"

# Count occurrences of XMAS and X-MAS
result_xmas, result_x_mas = count_xmas_and_xmas_occurrences(file_path)
print("Total occurrences of XMAS:", result_xmas)
print("Total occurrences of X-MAS:", result_x_mas)
