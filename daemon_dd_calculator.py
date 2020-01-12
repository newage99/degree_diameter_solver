from daemon import append_if_not_exists
from math import sqrt

n = 0
values = {}
results = []
degree_punctuation = 0
diameter_punctuation = 0
congestion_punctuation = 0


def calculate(adjacency_matrix):
    global n, degree_punctuation, diameter_punctuation, congestion_punctuation
    n = len(adjacency_matrix)
    distances = []
    degree_punctuation = 0
    for i in range(0, n):
        distances.append([-1] * n)
        distances[i][i] = 0
        node_degree = 0
        for j in range(0, n):
            if adjacency_matrix[i][j] > 0:
                distances[i][j] = 1
                node_degree += 1
        node_degree *= i
        degree_punctuation += node_degree
    highest_distance = -1
    distance_to_calculate = get_first_not_calculated_distance(distances)
    diameter_punctuation = 0
    congestion = [[0] * n]
    while distance_to_calculate is not None:
        visited_nodes = []
        to_visit_nodes = [distance_to_calculate[0]]
        distance = 0
        while distances[distance_to_calculate[0]][distance_to_calculate[1]] == -1:
            to_visit_aux = []
            to_visit_nodes_counter = 0
            temp = len(visited_nodes)
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
            for i in range(temp + 1, len(visited_nodes)):
                congestion[visited_nodes[i]] += 1
            to_visit_nodes = to_visit_aux
            distance += 1
        distance_to_calculate = get_first_not_calculated_distance(distances)
    congestion_punctuation = 0
    for i in range(0, n):
        congestion_punctuation += congestion[i]
        for j in range(0, n):
            diameter_punctuation += distances[i][j]


def get_first_not_calculated_distance(distances):
    global n
    for i in range(0, n):
        for j in range(i+1, n):
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


def find_gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def check_topology(id):
    total = degree_punctuation + diameter_punctuation
    # print(id + " " + degree_punctuation + " " + diameter_punctuation + " (")