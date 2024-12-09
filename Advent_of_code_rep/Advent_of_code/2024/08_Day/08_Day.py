def parse_map(map_input):
    """
    Parse the input map into a dictionary of frequencies and their locations.

    :param map_input: Multi-line string representing the map
    :return: Dictionary with frequencies as keys and lists of their locations as values
    """
    frequencies = {}
    for y, row in enumerate(map_input.strip().split('\n')):
        for x, char in enumerate(row):
            if char != '.':
                if char not in frequencies:
                    frequencies[char] = []
                frequencies[char].append((x, y))
    return frequencies


def find_antinodes(freq_locations):
    """
    Find antinodes for a specific frequency.

    :param freq_locations: List of (x, y) tuples for antennas of the same frequency
    :return: Set of unique antinode locations
    """
    antinodes = set()
    for i in range(len(freq_locations)):
        for j in range(i + 1, len(freq_locations)):
            x1, y1 = freq_locations[i]
            x2, y2 = freq_locations[j]

            # Calculate midpoint and direction
            dx = x2 - x1
            dy = y2 - y1

            # Midpoint
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            # Two possible antinodes (one on each side of the midpoint)
            antinode1_x = mid_x + dy
            antinode1_y = mid_y - dx

            antinode2_x = mid_x - dy
            antinode2_y = mid_y + dx

            antinodes.add((round(antinode1_x), round(antinode1_y)))
            antinodes.add((round(antinode2_x), round(antinode2_y)))

    return antinodes


def calculate_total_antinodes(map_input):
    """
    Calculate the total unique antinode locations in the map.

    :param map_input: Multi-line string representing the map
    :return: Number of unique antinode locations
    """
    # Parse the map into frequencies
    frequencies = parse_map(map_input)

    # Set to store unique antinode locations
    all_antinodes = set()

    # Find antinodes for each frequency group
    for freq, locations in frequencies.items():
        if len(locations) > 1:
            # Find antinodes for this frequency
            freq_antinodes = find_antinodes(locations)
            all_antinodes.update(freq_antinodes)

    return len(all_antinodes)


# Read input from test.txt
with open('test.txt', 'r') as file:
    input_map = file.read()

print("Total unique antinode locations:", calculate_total_antinodes(input_map))