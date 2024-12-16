
import argparse


DIRECTION_MAP = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}


def read_input(filename):
    """ read_input returns a grid as a list of strings, and steps as a string """
    with open(filename, 'r') as file:
        grid = []
        steps = []
        for line in file:
            if len(line) == 1:
                break
            grid.append(line.strip())
        for line in file:
            steps.append(line.strip())
    return grid, ''.join(steps)


def analyze_grid_str(grid_str):
    """ analyze_grid returns a list of character lists, and starting position"""
    start_pos = None
    for r, row in enumerate(grid_str):
        c = row.find('@')
        if c != -1:
            start_pos = (r, c)
            break

    return [list(row) for row in grid_str], start_pos


def expand_grid_str(grid_str):
    new_grid = []
    for row in grid_str:
        line = row
        line = line.replace("#", "##")
        line = line.replace("O", "[]")
        line = line.replace(".", "..")
        line = line.replace("@", "@.")
        new_grid.append(line)
    return new_grid


def calculate_gps_sum(grid):
    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'O' or cell == '[':
                total += (100 * r) + c
    return total


def part1(grid_str, steps):
    grid, start_pos = analyze_grid_str(grid_str)
    r, c = start_pos
    for step in steps:
        d = DIRECTION_MAP[step]
        nr, nc = r + d[0], c + d[1]

        if grid[nr][nc] == '#':
            continue
        if grid[nr][nc] == '.':
            grid[r][c] = '.'
            grid[nr][nc] = '@'
            r, c = nr, nc
            continue

        # Scan in direction until we hit "." or "#"
        peek_r, peek_c = nr + d[0], nc + d[1]
        while grid[peek_r][peek_c] != '.' and grid[peek_r][peek_c] != '#':
            peek_r, peek_c = peek_r + d[0], peek_c + d[1]

        if grid[peek_r][peek_c] == '.':
            grid[peek_r][peek_c] = 'O'
            grid[r][c] = '.'
            grid[nr][nc] = '@'
            r, c = nr, nc

    return calculate_gps_sum(grid)


def part2(grid_str, steps):

    expanded_grid_str = expand_grid_str(grid_str)
    grid, start_pos = analyze_grid_str(expanded_grid_str)

    r, c = start_pos
    for step in steps:
        d = DIRECTION_MAP[step]
        nr, nc, = r + d[0], c + d[1]

        # Immediately blocked
        if grid[nr][nc] == '#':
            continue

        # Simple left/right case
        if grid[nr][nc] == '.':
            grid[r][c] = '.'
            grid[nr][nc] = '@'
            r, c = nr, nc
            continue

        # Special cases
        ##################
        if d[1] != 0:  # Push box(es) left/right
            peek_c = nc

            # Peek until we see a blank space or a wall
            while grid[r][peek_c] != '.' and grid[r][peek_c] != '#':
                peek_c += d[1]

            # Boxes are flush against a wall, no movement
            if grid[r][peek_c] == '#':
                continue

            # If we hit an open space, shift the previous cells 1 unit over
            shift_c = peek_c
            while shift_c != c - d[1]:
                grid[r][shift_c] = grid[r][shift_c - d[1]]
                shift_c -= d[1]
            grid[r][c] = '.'
            c = nc

        else:  # Vertically shift boxes

            def get_shift_chain():
                """
                    This returns a dictionary of pieces that are valid to shift
                    otherwise None
                """
                queue = []
                queue.append((r, c))
                visited = {}
                visited[(nr, nc)] = grid[nr][nc]
                while queue:
                    cur_r, cur_c = queue.pop(0)
                    peek_r, peek_c = cur_r + d[0], cur_c + d[1]

                    if grid[peek_r][peek_c] == '#':
                        return None
                    if grid[peek_r][peek_c] == '.':
                        continue

                    visited[(peek_r, peek_c)
                            ] = grid[peek_r][peek_c]
                    if grid[peek_r][peek_c] == '[':
                        queue.append((peek_r, peek_c))
                        queue.append((peek_r, peek_c + 1))
                        visited[(peek_r, peek_c + 1)
                                ] = grid[peek_r][peek_c + 1]
                    elif grid[peek_r][peek_c] == ']':
                        queue.append((peek_r, peek_c))
                        queue.append((peek_r, peek_c - 1))
                        visited[(peek_r, peek_c - 1)
                                ] = grid[peek_r][peek_c - 1]
                return visited

            pieces_to_shift = get_shift_chain()
            if pieces_to_shift:
                for (pt, cell) in pieces_to_shift.items():
                    grid[pt[0]][pt[1]] = '.'
                for (pt, cell) in pieces_to_shift.items():
                    grid[pt[0] + d[0]][pt[1] + d[1]] = cell

                grid[r][c] = '.'
                grid[nr][c] = '@'
                r, c = nr, nc

    return calculate_gps_sum(grid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    grid_str, steps = read_input(args.filename)

    p1 = part1(grid_str, steps)
    print(f"Part1: sum = {p1}")

    p2 = part2(grid_str, steps)
    print(f"Part2: sum = {p2}")
