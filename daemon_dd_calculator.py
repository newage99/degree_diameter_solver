from daemon import append_if_not_exists
from math import sqrt

n = 0
values = {}


def calculate(adjacency_matrix):
    global n
    n = len(adjacency_matrix)
    distances = []
    degree = -1
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
    highest_distance = -1
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
    values[n] = [degree, diameter]


def get_first_not_calculated_distance(distances):
    global n
    for i in range(0, n):
        for j in range(0, n):
            if distances[i][j] == -1:
                return [i, j]
    return None


def check_if_constant(points):
    value = points[0][1]
    constant = True
    for i in range(1, len(points)):
        if value != points[i][1]:
            constant = False
            break
    return constant


def calculate_punctuation(points):
    if check_if_constant(points):
        return ["CONSTANT", points[0][1]]
    y1 = points[0][1]
    a = points[len(points) - 1][1] - y1
    x1 = points[len(points) - 1][0]
    b = x1 - points[0][0]
    sqrtab = sqrt((a*a) + (b*b))
    c = (a * x1) + (b * y1)
    last_under_or_above = 0
    first_one = True
    lowest_d = 0
    highest_d = 0
    total = 0
    print("a: " + str(a) + " | b: " + str(b) + " | c: " + str(c))
    for i in range(1, len(points)):
        x = points[i][0]
        y = points[i][1]
        d = abs((a * x) + (b * y) + c) / sqrtab
        if y < (a * x) + b:
            under_or_above = -1
            if d > lowest_d:
                lowest_d = d
        elif y > (a * x) + b:
            under_or_above = 1
            if d > highest_d:
                highest_d = d
        else:
            under_or_above = 0
        if first_one:
            first_one = False
        elif under_or_above != last_under_or_above:
            its_an_straight_line = False
            if last_under_or_above == 1:
                total += highest_d
            elif last_under_or_above == -1:
                total -= lowest_d
            lowest_d = 0
            highest_d = 0
        last_under_or_above = under_or_above
    return ["NO_CONST", total]


def check_topology(id):
    degree_points = []
    diameter_points = []
    for key in values:
        value = values[key]
        if value[0] > 0 and value[1] > 0:
            degree_points.append([key, value[0]])
            diameter_points.append([key, value[1]])
    if len(degree_points) >= 3:
        print(id)
        degree_result = calculate_punctuation(degree_points)
        print("degree: " + degree_result[0] + " " + str(degree_result[1]))
        diameter_result = calculate_punctuation(diameter_points)
        print("diameter: " + diameter_result[0] + " " + str(diameter_result[1]))
