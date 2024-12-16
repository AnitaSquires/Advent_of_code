import numpy as np

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
        perimeter = 0
        while cells_to_process:
            c = cells_to_process.pop()
            for d in {(-1,0), (1,0), (0,-1), (0,1)}:
                if (c[0] + d[0], c[1] + d[1]) in current_region:
                    pass
                elif c[0] + d[0] < 0 or c[0] + d[0] >= rows \
                    or c[1] + d[1] < 0 or c[1] + d[1] >= cols \
                        or garden[c[0] + d[0], c[1] + d[1]] != current_crop:
                    perimeter += 1
                else:
                    cells_to_process.add((c[0] + d[0], c[1] + d[1]))
            current_region.add(c)
            garden[c] = ord('.')
        area = len(current_region)
        total_cost += perimeter * area
print("Part 1 results= ",total_cost)