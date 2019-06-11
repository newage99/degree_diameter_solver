import daemon_tcp

daemon_on = True


def append_if_not_exists(array, value):
    not_visited = True
    for node in array:
        if node == value:
            not_visited = False
            break
    if not_visited:
        array.append(value)
    return array


if __name__ == "__main__":
    daemon_tcp.init()
