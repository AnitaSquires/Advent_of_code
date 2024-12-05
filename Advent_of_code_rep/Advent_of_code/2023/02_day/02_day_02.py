# Read the input from a file (assuming input.txt is in the same directory)
input_file = "input"

valid_game_ids = []

# Open and read the file
with open(input_file, "r") as file:
    games_input = file.readlines()

# Initialize variable to store the sum of the powers
total_power = 0

# Process each game
for game in games_input:
    game = game.strip()  # Remove any extra whitespace or newlines

    if not game:  # Skip empty lines
        continue

    try:
        # Split the game data into the game ID and revealed sets
        game_id, revealed_sets = game.split(": ", 1)

        # Split the revealed sets by ';' to process each individual set
        sets = revealed_sets.split(";")

        # Initialize the maximum values for red, green, and blue cubes
        max_red = 0
        max_green = 0
        max_blue = 0

        # Process each set of revealed cubes
        for set_info in sets:
            cubes = set_info.split(", ")

            # Track the maximum cubes for each color in this set
            red, green, blue = 0, 0, 0
            for cube in cubes:
                count, color = cube.split()
                count = int(count)

                if color == "red":
                    red = count
                elif color == "green":
                    green = count
                elif color == "blue":
                    blue = count

            # Update the maximum values for each color
            max_red = max(max_red, red)
            max_green = max(max_green, green)
            max_blue = max(max_blue, blue)

        # Calculate the power for this game (product of max red, green, blue cubes)
        power = max_red * max_green * max_blue
        total_power += power

    except ValueError as e:
        # Handle error case: print a message if the line cannot be split properly
        print(f"Error processing game line: {game} - {e}")

# Output the final sum of powers for all games
print("Sum of the powers:", total_power)