import threading
import requests
import socket
import jsons
import time

daemon_on = True
topology_id = ["x", "x", "x"]
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
    "1": numbers_array,
    "2": numbers_array,
    "5": numbers_array,
    "7": numbers_array
}
xyn_array_left = ["x", "y", "n", ")", "1", "2", "5", "7"]
operators_array_left = ["+", "-", "*", "/", "%", "("]
numbers_array_left = ["x", "y", "n", ")", "1", "2", "5", "7"]
sum_close_parenthesis_left = ["+", "-", "*", "/", "%", "("]
forbidden_left_chars = {
    "x": xyn_array_left,
    "y": xyn_array_left,
    "n": xyn_array_left,
    "+": sum_close_parenthesis_left,
    "-": ["+", "-"],
    "*": operators_array_left,
    "/": operators_array_left,
    "%": operators_array_left,
    "(": ["x", "y", "n", ")", "1", "2", "5", "7"],
    ")": sum_close_parenthesis_left,
    "1": numbers_array_left,
    "2": numbers_array_left,
    "5": numbers_array_left,
    "7": numbers_array_left
}

calculation_thread = None
calculation_on = True
length = 0
every = None
results = []
characters = ""
beginning = None


def get_master_ip():
    return jsons.loads(requests.get("http://myaurea.es/wp-json/wp/v2/posts?id=12535").text)[0]["title"]["rendered"]


def calculation_func():
    global length, every, characters, beginning, calculation_on, calculation_thread, results
    if length is not None and length > 0 and every is not None and every > 0 and characters is not None \
            and len(characters) > 0 and beginning is not None and len(beginning) > 0:
        topology_id.clear()
        for char in beginning.decode("utf-8"):
            topology_id.append(char)
        returned_true = True
        str = "".join(topology_id)
        while calculation_on and returned_true:
            pointer = validate_string(str)
            if pointer is 0:
                results.append(str)
            returned_true, str = next_string(str, pointer)
        a = 0


def tcp_handler(s):
    global length, every, characters, beginning, calculation_on, calculation_thread
    print("Correctly connected to master.")
    while daemon_on:
        s.settimeout(None)
        response = s.recv(65536)
        length = response[0]
        every = int.from_bytes(response[1:3], byteorder='big')
        characters_length_final = 4 + response[3]
        characters = response[4:characters_length_final].decode("utf-8")
        beginning = response[characters_length_final:characters_length_final+length]
        if calculation_thread is not None:
            calculation_on = False
            calculation_thread.join()
        calculation_thread = threading.Thread(target=calculation_func)
        calculation_thread.start()


def communication_with_master_thread():
    while daemon_on:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # s.connect((get_master_ip(), 9999))
                s.connect(("localhost", 9999))
                tcp_handler(s)
        except Exception as e:
            print("communication_with_master_thread: " + str(e))
        time.sleep(120)


def validate_string(str):
    if str == "x*-":
        a = 0
    prev = " "
    actual = str[0]
    nextt = None
    prevString = ''
    nextString = ''
    numOpeningParentesis = 0
    numClosingParentesis = 0
    for i in range(1, length + 1):
        if i < len(str):
            nextt = str[i]
        else:
            nextt = " "
        prevString = forbidden_left_chars[actual]
        nextString = forbidden_right_chars[actual]
        if prev in prevString or nextt in nextString:
            return i
        prev = actual
        actual = nextt
    # POST CHECK 0
    last = str[-1]
    if last == "+" or last == "-" or last == "*" or last == "/" or last == "%" or last == "(":
        return length - 1
    # POST CHECK 1
    if "x" not in str or "y" not in str:
        return length - 1
    # POST CHECK 2
    if("y" in str and "x" not in str) or (("z" in str) and ("x" not in str or "y" not in str)):
        return length - 1
    # POSTCHECK 3
    containsVariables = False
    wrongParentesis = False
    parentesisCounter = 0
    parentesisWithOneSpaceOnly = False
    varsSinceLastOpeningParentesis = 0
    last = " "
    empiezaDobleParentesis = False
    hayUnDobleParentesis = False
    for chr in str:
        if chr in "xyzn":
            containsVariables = True
        if chr is "(":
            parentesisCounter += 1
            varsSinceLastOpeningParentesis = 0
            if last is "(":
                empiezaDobleParentesis = True
        else:
            if chr is ")":
                if last is ")" and empiezaDobleParentesis:
                    hayUnDobleParentesis = True
                    break
                parentesisCounter -= 1
                if varsSinceLastOpeningParentesis < 2:
                    parentesisWithOneSpaceOnly = True
                    break
            else:
                if last is ")":
                    empiezaDobleParentesis = False
                    break
                varsSinceLastOpeningParentesis += 1
        if parentesisCounter < 0:
            wrongParentesis = True
            break
        last = chr
    # POST CHECKS 4
    if not containsVariables or wrongParentesis or parentesisCounter is not 0 or parentesisWithOneSpaceOnly or hayUnDobleParentesis:
        return length - 1
    if str.startswith("(") and str.endswith(")"):
        return length - 1
    return 0


def next_string(str, pointer):
    model_pos = -1
    if pointer < length - 1:
        if pointer > 0:
            aux = ""
            for i in range(pointer + 1, length):
                aux += characters[0]
            str = str[0:pointer + 1] + aux
        else:
            pointer = length - 1
    else:
        pointer = length - 1
    while pointer >= 0:
        char_to_look_at = str[pointer]
        for i in range(0, len(characters)):
            if characters[i] is char_to_look_at:
                model_pos = i
                break
        if model_pos < len(characters) - 1:
            str = str[0:pointer] + characters[model_pos + 1]
            for i in range(0, length - len(str)):
                str += characters[0]
            return True, str
        else:
            pointer -= 1
    return False, str


if __name__ == "__main__":
    # We start the thread that will establish the communication with the Master
    threading.Thread(target=communication_with_master_thread).start()
