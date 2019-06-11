from daemon import append_if_not_exists

n = 0


def calculate(id, adjacency_matrix):
    global n
    n = len(adjacency_matrix)
    distances = []
    degree = 1
    for i in range(0, n):
        distances.append([-1] * n)
        distances[i][i] = 0
        node_degree = 0
        for j in range(0, n):
            if adjacency_matrix[i][j] >= 1:
                distances[i][j] = 1
                node_degree += 1
        if node_degree > degree:
            degree = node_degree
    highest_distance = 1
    distance_to_calculate = get_first_not_calculated_distance(distances)
    while distance_to_calculate is not None:
        visited_nodes = []
        to_visit_nodes = [distance_to_calculate[0]]
        distance = 0
        while distances[distance_to_calculate[0]][distance_to_calculate[1]] == -1:
            to_visit_aux = []
            to_visit_nodes_counter = 0
            while to_visit_nodes_counter < len(to_visit_nodes):
                actual_node = to_visit_nodes[to_visit_nodes_counter]
                row = adjacency_matrix[actual_node]
                for i in range(0, n):
                    if row[i] >= 1:
                        if i not in visited_nodes:
                            to_visit_aux = append_if_not_exists(to_visit_aux, i)
                        if i == distance_to_calculate[1]:
                            distances[distance_to_calculate[0]][i] = distance
                            distances[i][distance_to_calculate[0]] = distance
                            if distance > highest_distance:
                                highest_distance = distance
                            to_visit_nodes_counter = len(to_visit_nodes)
                            break
                visited_nodes = append_if_not_exists(visited_nodes, actual_node)
                to_visit_nodes_counter += 1
            to_visit_nodes = to_visit_aux
            distance += 1
        distance_to_calculate = get_first_not_calculated_distance(distances)
    diameter = highest_distance
    # TODO


def get_first_not_calculated_distance(distances):
    global n
    for i in range(0, n):
        for j in range(0, n):
            if distances[i][j] == -1:
                return [i, j]
    return None


def check_topology():
    pass