from daemon import append_if_not_exists
from math import sqrt

n = 0
values = {}
results = []


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


def find_gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def calculate_punctuation(points):
    if check_if_constant(points):
        return ["CONSTANT", points[0][1]]
    x1 = points[0][0]
    x2 = points[-1][0]
    a = x1 - x2
    y1 = points[0][1]
    b = points[-1][1] - y1
    c = (a * y1) + (b * x1)
    sqrtab = sqrt((a * a) + (b * b))
    last_under_or_above = 0
    first_one = True
    lowest_d = 0
    highest_d = 0
    total = 0
    # print("a: " + str(a) + " | b: " + str(b) + " | c: " + str(c))
    for i in range(1, len(points)):
        if c == -80:
            t = 0
        x = points[i][0]
        y = points[i][1]
        d = abs((a * y) + (b * x) - c) / sqrtab
        comp = ((b * x) - c) / -a
        if y < comp:
            under_or_above = -1
            if d > lowest_d:
                lowest_d = d
        elif y > comp:
            under_or_above = 1
            if d > highest_d:
                highest_d = d
        else:
            under_or_above = 0
        if first_one:
            if under_or_above != 0:
                first_one = False
        elif under_or_above != last_under_or_above:
            if last_under_or_above == 1:
                total += highest_d
            elif last_under_or_above == -1:
                total -= lowest_d
            lowest_d = 0
            highest_d = 0
        last_under_or_above = under_or_above
    return ["NO_CONST", total]


def compare_results(first, second):
    if first[0] == "CONSTANT":
        if second[0] != "CONSTANT" or first[1] < second[1]:
            return "BEST"
        elif first[1] > second[1]:
            return "WORST"
        else:
            return "EQUAL"
    elif second[0] == "CONSTANT" or first[1] < second[1]:
        return "WORST"
    elif first[1] > second[1]:
        return "BEST"
    else:
        return "EQUAL"


def insert_into_results_list(id, degree_results, diameter_results):
    pos = -1
    my_num_constants = 1 if degree_results[0] == "CONSTANT" else 0
    my_num_constants += 1 if diameter_results[0] == "CONSTANT" else 0
    not_added = True
    for i in range(len(results) - 1):
        actual = results[i]
        num_constants = 1 if actual[0][0] == "CONSTANT" else 0
        num_constants += 1 if actual[1][0] == "CONSTANT" else 0
        comp_1 = compare_results(degree_results, actual[0])
        comp_2 = compare_results(diameter_results, actual[1])
        if (comp_1 == "BEST" and comp_2 == "BEST") or my_num_constants > num_constants:
            pos = i
            break
        elif my_num_constants == num_constants:
            if my_num_constants == 1:
                # TODO
                t = 0
            else:
                my_degree = degree_results[1]
                my_diameter = diameter_results[1]
                if my_degree == actual[0][1] and my_diameter == actual[1][1]:
                    results[i][2].append(id)
                    not_added = False
                elif my_degree == actual[1][1] and my_diameter == actual[0][1]:
                    if i < len(results) - 1:
                        if my_degree == results[i+1][0][1] and my_diameter == results[i+1][1][1]:
                            results[i+1][2].append(id)
                            not_added = False
                            break
                        else:
                            pos = i + 1
                            break
                    else:
                        break
                elif my_degree[0] == "CONSTANT" and my_diameter[0] == "CONSTANT":
                    if my_degree[1] + my_diameter[1] < actual[0][1] + actual[1][1]:
                        pos = i
                        break
                elif my_degree[1] + my_diameter[1] > actual[0][1] + actual[1][1]:
                    pos = i
                    break


    if not_added:
        if pos == -1 or pos >= len(results):
            results.append([degree_results, diameter_results, [id]])
        else:
            results.insert(pos, [degree_results, diameter_results, [id]])


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
        insert_into_results_list(id, degree_result, diameter_result)
