import daemon_dd_calculator
from daemon import append_if_not_exists

sizes = []
exec_result = None


def set_sizes(sizess):
    global sizes
    sizes = sizess


def is_graph_connected(adjacency_matrix):
    if adjacency_matrix is None or len(adjacency_matrix) <= 1:
        return False
    for row in adjacency_matrix:
        no_neighbours = True
        for node in row:
            if node >= 1:
                no_neighbours = False
        if no_neighbours:
            return False
    if len(adjacency_matrix) == 20:
        a = 0
    visited_nodes = [0]
    visited_nodes_counter = 0
    while visited_nodes_counter < len(visited_nodes):
        neighs = adjacency_matrix[visited_nodes[visited_nodes_counter]]
        for i in range(0, len(neighs)):
            if neighs[i] >= 1:
                visited_nodes = append_if_not_exists(visited_nodes, i)
                if len(visited_nodes) == len(adjacency_matrix):
                    return True
        visited_nodes_counter += 1
    return len(visited_nodes) == len(adjacency_matrix)


def create_topology(id, n):
    global exec_result
    adjancency_matrix = []
    for i in range(0, n):
        adjancency_matrix.append([0] * n)
    for x in range(0, n):
        for y in range(x, n):
            try:
                exec("global exec_result; exec_result = " +
                     id.replace("x", "float(x)")
                     .replace("y", "float(y)")
                     .replace("n", "float(n)"))
                exec_result = int(round(exec_result))
                if 0 <= exec_result < n and exec_result != x:
                    if adjancency_matrix[x][exec_result] == 0:
                        adjancency_matrix[x][exec_result] = 1
                    else:
                        adjancency_matrix[x][exec_result] += 1
                    adjancency_matrix[exec_result][x] = adjancency_matrix[x][exec_result]
            except:
                pass
    if is_graph_connected(adjancency_matrix):
        daemon_dd_calculator.calculate(id, adjancency_matrix)


def create(id):
    global sizes
    if len(sizes) < 2:
        return
    for size in sizes:
        create_topology(id, size)
    daemon_dd_calculator.check_topology()
