import daemon_topology_creator
import threading
import random
import time

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


def compute(lengthh, characterss, sizee):
    global length, characters, beginning, size, calculation_thread, calculation_on
    length = lengthh
    characters = characterss
    size = sizee
    if calculation_thread is not None:
        calculation_on = False
        calculation_thread.join()
    calculation_thread = threading.Thread(target=calculation_func)
    calculation_thread.start()


def calculation_func():
    global length, characters, size, calculation_on, calculation_thread
    if length is not None and length > 0 and characters is not None and len(characters) > 0 and size > 0:
        # daemon_topology_creator.set_size(size)
        while calculation_on:
            # if validate_id(topology_id):
            #     daemon_topology_creator.create(topology_id)
            print(random_id())
            time.sleep(1)


def mutate_id(id):
    pass


def random_id():
    new_id, is_open_parenthesis, is_close_parenthesis = random_char()
    parenthesis_counter = 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
    while new_id in plus_minus_array:
        new_id, is_open_parenthesis, is_close_parenthesis = random_char()
        parenthesis_counter = 1 if is_open_parenthesis else 0
    while len(new_id) < length or new_id[-1] in operators_array_left:
        new_c, is_open_parenthesis, is_close_parenthesis = random_char()
        while new_id[-1] in forbidden_left_chars[new_c] or \
                (is_close_parenthesis and not valid_close_parenthesis(new_id, parenthesis_counter)) or \
                (is_open_parenthesis and not valid_open_parenthesis(new_id, parenthesis_counter)):
            new_c, is_open_parenthesis, is_close_parenthesis = random_char()
        parenthesis_counter += 1 if is_open_parenthesis else -1 if is_close_parenthesis else 0
        new_id += new_c
    while parenthesis_counter > 0:
        if new_id[-1] in forbidden_left_chars[")"]:
            new_c, is_open_parenthesis, is_close_parenthesis = random_char()
            while new_id[-1] in forbidden_left_chars[new_c] or new_c == "(":
                new_c, is_open_parenthesis, is_close_parenthesis = random_char()
            new_id += new_c
        else:
            new_id += ")"
            parenthesis_counter -= 1
    return new_id


def valid_close_parenthesis(id, parenthesis_counter):
    if parenthesis_counter > 0:
        length_check = 0
        valid = True
        while length_check < 3 and valid:
            if len(id) > length_check and id[-(length_check+1)] == '(':
                valid = False
            length_check += 1
        if valid:
            return True
    return False


def valid_open_parenthesis(id, parenthesis_counter):
    remain_to_fill = length - len(id)
    remain_to_fill = 0 if remain_to_fill < 0 else remain_to_fill
    return parenthesis_counter < remain_to_fill - 3


def random_char():
    new_c = characters[random.randint(0, len(characters) - 1)]
    return new_c, new_c == '(', new_c == ')'


def validate_id(id):
    global length
    # PRE CHECK 1
    start = id[0]
    if start == "+" or start == "*" or start == "/" or start == "%" or start == ")":
        return False
    prev = " "
    actual = id[0]
    for i in range(1, length + 1):
        if i < len(id):
            nextt = id[i]
        else:
            nextt = " "
        if prev in forbidden_left_chars[actual] or nextt in forbidden_right_chars[actual]:
            return False
        prev = actual
        actual = nextt
    # POST CHECK 0
    last = id[-1]
    if last == "+" or last == "-" or last == "*" or last == "/" or last == "%" or last == "(":
        return False
    # POST CHECK 1
    if "x" not in id or "y" not in id:
        return False
    # POST CHECK 2
    if("y" in id and "x" not in id) or (("z" in id) and ("x" not in id or "y" not in id)):
        return False
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
        return False
    if id.startswith("(") and id.endswith(")"):
        return False
    return True


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
