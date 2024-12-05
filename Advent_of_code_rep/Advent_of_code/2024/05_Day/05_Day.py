def parse_input(input_file):
    """
    Parse the input file into rules and updates.

    Args:
        input_file (str): Path to the input file.

    Returns:
        tuple: A tuple containing:
            - rules (list of tuples): A list of (X, Y) rules indicating X|Y relationships.
            - updates (list of lists): A list of updates, each containing a list of page numbers.
    """
    with open(input_file, 'r') as file:
        data = file.read().strip()
    rules_section, updates_section = data.split("\n\n")

    # Parse rules
    rules = []
    for line in rules_section.splitlines():
        x, y = map(int, line.split("|"))
        rules.append((x, y))

    # Parse updates
    updates = []
    for line in updates_section.splitlines():
        updates.append(list(map(int, line.split(","))))

    return rules, updates


def is_valid_update(update, rules):
    """
    Check if an update is valid according to the rules.

    Args:
        update (list of int): The page numbers in the update.
        rules (list of tuples): A list of (X, Y) rules indicating X|Y relationships.

    Returns:
        bool: True if the update is valid, False otherwise.
    """
    for x, y in rules:
        # Check if both pages are in the update
        if x in update and y in update:
            # Ensure x comes before y
            if update.index(x) > update.index(y):
                return False
    return True


def middle_page(update):
    """
    Get the middle page of an update.

    Args:
        update (list of int): The page numbers in the update.

    Returns:
        int: The middle page number.
    """
    mid_index = len(update) // 2
    return update[mid_index]


def reorder_update(update, rules):
    """
    Reorder an invalid update according to the rules.

    Args:
        update (list of int): The page numbers in the update.
        rules (list of tuples): A list of (X, Y) rules indicating X|Y relationships.

    Returns:
        list of int: The reordered update.
    """
    # Convert the rules to a dependency graph
    from collections import defaultdict, deque

    graph = defaultdict(list)
    indegree = defaultdict(int)

    # Build the graph
    for x, y in rules:
        if x in update and y in update:
            graph[x].append(y)
            indegree[y] += 1
            indegree[x]  # Ensure x is included in indegree dictionary

    # Topological sort using Kahn's Algorithm
    sorted_update = []
    queue = deque(page for page in update if indegree[page] == 0)

    while queue:
        current = queue.popleft()
        sorted_update.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update


def calculate_updates(input_file):
    """
    Calculate the sum of middle pages for valid and corrected updates.

    Args:
        input_file (str): Path to the input file.

    Returns:
        tuple: A tuple containing:
            - valid_total_middle (int): Sum of middle pages for valid updates.
            - invalid_total_middle (int): Sum of middle pages for corrected updates.
    """
    rules, updates = parse_input(input_file)
    valid_total_middle = 0
    invalid_total_middle = 0

    for update in updates:
        if is_valid_update(update, rules):
            # Valid updates
            valid_total_middle += middle_page(update)
        else:
            # Invalid updates
            corrected_update = reorder_update(update, rules)
            invalid_total_middle += middle_page(corrected_update)

    return valid_total_middle, invalid_total_middle


# Specify the input file
if __name__ == "__main__":
    input_file = "input.txt"
    valid_total, invalid_total = calculate_updates(input_file)
    print("Sum of middle pages from valid updates:", valid_total)
    print("Sum of middle pages from corrected updates:", invalid_total)
