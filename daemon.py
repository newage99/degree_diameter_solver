import threading

characters = "xyn+-*/%()1257"
characters_length = len(characters)
actual_topology_id = ["x", "x", "x"]
length = 3
send_every_seconds = 0
adjacency_matrix = []
results = []
xyn_array = ["x", "y", "n", "(", "1", "2", "5", "7"]
plus_minus_array = ["+", "-", "*", "/", "%", ")"]
operators_array = ["+", "*", "/", "%", ")"]
numbers_array = ["x", "y", "n", "1", "2", "5", "7"]
forbidden_right_chars = {
    "x": xyn_array,
    "y": xyn_array,
    "n": xyn_array,
    "+": plus_minus_array,
    "-": plus_minus_array,
    "*": operators_array,
    "/": operators_array,
    "%": operators_array,
    "(": ["+", "*", "/", "%", ")"],
    ")": ["x", "y", "n", "1", "2", "5", "7"],
    "1": numbers_array
}


def communication_with_master_thread():
    a = 0


def add_or_subtract_because_of_parenthesis(char, value):
    if char == "(":
        return value + 1, True
    elif char == ")":
        return value - 1, True
    return value, False


def set_next_id():
    wrong_position = -1
    parenthesis_counter = 0
    last_parenthesis_position = -1
    for i in range(length):
        if i < length - 1 and actual_topology_id[i+1] in forbidden_right_chars[actual_topology_id[i]]:
            wrong_position = i+1
            break
        (parenthesis_counter, there_is_a_parenthesis) = \
            add_or_subtract_because_of_parenthesis(actual_topology_id[i], parenthesis_counter)
        if there_is_a_parenthesis:
            last_parenthesis_position = i

    start = length - 1

    if wrong_position > -1 and parenthesis_counter != 0:
        start = min(wrong_position, last_parenthesis_position)
    elif wrong_position > -1:
        start = wrong_position
    elif parenthesis_counter != 0:
        start = last_parenthesis_position

    for i in range(start, -1, -1):
        last_char_position = characters.find(actual_topology_id[i])
        if last_char_position < characters_length - 1:
            actual_topology_id[i] = characters[last_char_position + 1]
            for j in range(i + 1, length):
                actual_topology_id[j] = characters[0]
                return True
    return False


def create_next_adjacency_matrix():
    if set_next_id():
        print("".join(actual_topology_id))
        return True
    return False


if __name__ == "__main__":
    # We start the thread that will establish the communication with the Master
    threading.Thread(target=communication_with_master_thread).start()
