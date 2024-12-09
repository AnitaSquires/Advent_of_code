def update_gitignore(entries):
    """
    Add specified entries to the .gitignore file if they are not already present.

    Args:
        entries (list of str): A list of file patterns or file names to add to .gitignore.
    """
    gitignore_path = "Advent_of_code_rep/.gitignore"

    try:
        # Read existing entries from .gitignore if it exists
        try:
            with open(gitignore_path, "r") as file:
                existing_entries = file.read().splitlines()
        except FileNotFoundError:
            existing_entries = []  # No .gitignore file exists yet

        # Open .gitignore in append mode and add missing entries
        with open(gitignore_path, "a") as file:
            for entry in entries:
                if entry not in existing_entries:
                    file.write(entry + "\n")
                    print(f"Added {entry} to .gitignore.")
                else:
                    print(f"{entry} is already in .gitignore.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
entries_to_add = ["test.txt", "input.txt", "*.log"]
update_gitignore(entries_to_add)