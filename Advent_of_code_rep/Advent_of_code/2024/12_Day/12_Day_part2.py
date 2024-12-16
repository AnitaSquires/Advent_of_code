import numpy as np

RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3

with open('input.txt', 'r') as f:
    lines = f.read().split('\n')

rows = len(lines)
cols = len(lines[0])
garden = np.empty((rows, cols), dtype=int)
for i, L in enumerate(lines):
    for j, c in enumerate(L):
        garden[i,j] = ord(c)

total_cost = 0
for i in range(rows):
    for j in range(cols):
        if garden[i,j] == ord('.'):
            continue

        current_crop = garden[i,j]
        cells_to_process = {(i,j)}
        current_region = set()
        current_boundary = set()
        while cells_to_process:
            c = cells_to_process.pop()
            for d in {(-1,0), (1,0), (0,-1), (0,1)}:
                if (c[0] + d[0], c[1] + d[1]) in current_region:
                    pass
                elif c[0] + d[0] < 0 or c[0] + d[0] >= rows \
                    or c[1] + d[1] < 0 or c[1] + d[1] >= cols \
                        or garden[c[0] + d[0], c[1] + d[1]] != current_crop:
                    current_boundary.add((c[0] + 0.5 * d[0], c[1] + 0.5 * d[1]))
                else:
                    cells_to_process.add((c[0] + d[0], c[1] + d[1]))
            current_region.add(c)
            garden[c] = ord('.')

        sides = 0
        while current_boundary:
            # find starting point for tracing boundary
            b = current_boundary.pop()
            if b[0].is_integer():
                if (int(b[0]), int(b[1] - 0.5)) in current_region:
                    start = (int(b[0]), int(b[1] - 0.5))
                    facing_start = DOWN
                else:
                    start = (int(b[0]), int(b[1] + 0.5))
                    facing_start = UP
            else:
                if (int(b[0] - 0.5), int(b[1])) in current_region:
                    start = (int(b[0] - 0.5), int(b[1]))
                    facing_start = LEFT
                else:
                    start = (int(b[0] + 0.5), int(b[1]))
                    facing_start = RIGHT
            # find the number of sides in the boundary
            # concept is walking around the enclosed region, always
            # keeping our right hand inside the region
            c = start
            facing = facing_start
            while True:
                if facing == RIGHT:
                    current_boundary.discard((c[0] - 0.5, c[1]))
                    if (c[0], c[1] + 1) not in current_region:
                        sides += 1
                        facing = DOWN
                    elif (c[0] - 1, c[1] + 1) not in current_region:
                        c = (c[0], c[1] + 1)
                    else:
                        sides += 1
                        facing = UP
                        c = (c[0] - 1, c[1] + 1)
                elif facing == DOWN:
                    current_boundary.discard((c[0], c[1] + 0.5))
                    if (c[0] + 1, c[1]) not in current_region:
                        sides += 1
                        facing = LEFT
                    elif (c[0] + 1, c[1] + 1) not in current_region:
                        c = (c[0] + 1, c[1])
                    else:
                        sides += 1
                        facing = RIGHT
                        c = (c[0] + 1, c[1] + 1)
                elif facing == LEFT:
                    current_boundary.discard((c[0] + 0.5, c[1]))
                    if (c[0], c[1] - 1) not in current_region:
                        sides += 1
                        facing = UP
                    elif (c[0] + 1, c[1] - 1) not in current_region:
                        c = (c[0], c[1] - 1)
                    else:
                        sides += 1
                        facing = DOWN
                        c = (c[0] + 1, c[1] - 1)
                else:       # facing UP
                    current_boundary.discard((c[0], c[1] - 0.5))
                    if (c[0] - 1, c[1]) not in current_region:
                        sides += 1
                        facing = RIGHT
                    elif (c[0] - 1, c[1] - 1) not in current_region:
                        c = (c[0] - 1, c[1])
                    else:
                        sides += 1
                        facing = LEFT
                        c = (c[0] - 1, c[1] - 1)
                if c == start and facing == facing_start:
                    break

        area = len(current_region)
        total_cost += sides * area
print(total_cost)