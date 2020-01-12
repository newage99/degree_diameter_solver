import daemon_topology_creator
import threading
import random import randint

variables = ["x", "y", "n"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
numbers_array = variables + numbers
xyn_array = numbers_array + ["("]
plus_minus_array = ["+", "-", "*", "/", "%", ")"]
operators_array = ["+", "*", "/", "%", ")"]
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
    ")": numbers_array,
    "0": numbers_array,
    "1": numbers_array,
    "2": numbers_array,
    "3": numbers_array,
    "4": numbers_array,
    "5": numbers_array,
    "6": numbers_array,
    "7": numbers_array,
    "8": numbers_array,
    "9": numbers_array
}
array_left = variables + [")"] + numbers
xyn_array_left = variables + [")"] + numbers
operators_array_left = ["+", "-", "*", "/", "%", "("]
sum_close_parenthesis_left = ["+", "-", "*", "/", "%", "("]
forbidden_left_chars = {
    "x": array_left,
    "y": array_left,
    "n": array_left,
    "+": sum_close_parenthesis_left,
    "-": ["+", "-"],
    "*": operators_array_left,
    "/": operators_array_left,
    "%": operators_array_left,
    "(": array_left,
    ")": sum_close_parenthesis_left,
    "0": array_left,
    "1": array_left,
    "2": array_left,
    "3": array_left,
    "4": array_left,
    "5": array_left,
    "6": array_left,
    "7": array_left,
    "8": array_left,
    "9": array_left
}
length = 0
every = 0
characters = ""
beginning = ""
size = []
calculation_thread = None
calculation_on = True


def compute(lengthh, characterss, beginningg, sizee):
    global length, every, characters, beginning, size, calculation_thread, calculation_on
    length = lengthh
    characters = characterss
    beginning = beginningg
    size = sizee
    if calculation_thread is not None:
        calculation_on = False
        calculation_thread.join()
    calculation_thread = threading.Thread(target=calculation_func)
    calculation_thread.start()


def calculation_func():
    global length, every, characters, beginning, size, calculation_on, calculation_thread
    if length is not None and length > 0 and every is not None and every > 0 and characters is not None \
            and len(characters) > 0 and beginning is not None and len(beginning) > 0 and size > 0:
        returned_true = True
        beginning_len = len(beginning)
        if beginning_len < length:
            beginning += characters[0] * (length - beginning_len)
        topology_id = beginning
        daemon_topology_creator.set_size(size)
        while calculation_on and returned_true:
            pointer = validate_id(topology_id)
            if pointer is 0:
                daemon_topology_creator.create(topology_id)
            returned_true, topology_id = next_id(topology_id, pointer)


def random_id():
    pass
    # TODO


def validate_id(id):
    global length
    # PRE CHECK 1
    start = id[0]
    if start == "+" or start == "*" or start == "/" or start == "%" or start == ")":
        return length - 1
    prev = " "
    actual = id[0]
    for i in range(1, length + 1):
        if i < len(id):
            nextt = id[i]
        else:
            nextt = " "
        if prev in forbidden_left_chars[actual] or nextt in forbidden_right_chars[actual]:
            return i
        prev = actual
        actual = nextt
    # POST CHECK 0
    last = id[-1]
    if last == "+" or last == "-" or last == "*" or last == "/" or last == "%" or last == "(":
        return length - 1
    # POST CHECK 1
    if "x" not in id or "y" not in id:
        return length - 1
    # POST CHECK 2
    if("y" in id and "x" not in id) or (("z" in id) and ("x" not in id or "y" not in id)):
        return length - 1
    # POST CHECK 3
    contains_variables = False
    wrong_parenthesis = False
    parenthesis_counter = 0
    parenthesis_with_one_space_only = False
    vars_since_last_opening_parenthesis = 0
    last = " "
    double_parenthesis_starts = False
    there_is_a_double_parenthesis = False
    for c in id:
        if c in "xyzn":
            contains_variables = True
        if c is "(":
            parenthesis_counter += 1
            vars_since_last_opening_parenthesis = 0
            if last is "(":
                double_parenthesis_starts = True
        else:
            if c is ")":
                if last is ")" and double_parenthesis_starts:
                    there_is_a_double_parenthesis = True
                    break
                parenthesis_counter -= 1
                if vars_since_last_opening_parenthesis < 2:
                    parenthesis_with_one_space_only = True
                    break
            else:
                if last is ")":
                    double_parenthesis_starts = False
                    break
                vars_since_last_opening_parenthesis += 1
        if parenthesis_counter < 0:
            wrong_parenthesis = True
            break
        last = c
    # POST CHECKS 4
    if not contains_variables or wrong_parenthesis or parenthesis_counter is not 0 \
            or parenthesis_with_one_space_only or there_is_a_double_parenthesis:
        return length - 1
    if id.startswith("(") and id.endswith(")"):
        return length - 1
    return 0


def next_id(id, pointer):
    global characters
    model_pos = -1
    if pointer < length - 1:
        if pointer > 0:
            aux = ""
            for i in range(pointer + 1, length):
                aux += characters[0]
            id = id[0:pointer + 1] + aux
        else:
            pointer = length - 1
    else:
        pointer = length - 1
    while pointer >= 0:
        char_to_look_at = id[pointer]
        for i in range(0, len(characters)):
            if characters[i] is char_to_look_at:
                model_pos = i
                break
        if model_pos < len(characters) - 1:
            id = id[0:pointer] + characters[model_pos + 1]
            for i in range(0, length - len(id)):
                id += characters[0]
            return True, id
        else:
            pointer -= 1
    return False, id
