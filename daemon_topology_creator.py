import daemon_dd_calculator

sizes = []
exec_result = None


def set_sizes(sizess):
    global sizes
    sizes = sizess


def create_topology(id, n):
    global exec_result
    adjancency_matrix = []
    for i in range(0, n):
        row = []
        for j in range(n):
            row.append(0)
        adjancency_matrix.append(row)
    for x in range(0, n):
        for y in range(x, n):
            try:
                exec("global exec_result; exec_result = " +
                     id.replace("x", "float(x)")
                     .replace("y", "float(y)")
                     .replace("n", "float(n)"))
                exec_result = round(exec_result)
                if 0 <= exec_result < n:
                    if adjancency_matrix[x][exec_result] == 0:
                        adjancency_matrix[x][exec_result] = 1
                    else:
                        adjancency_matrix[x][exec_result] += 1
                    adjancency_matrix[exec_result][x] = adjancency_matrix[x][exec_result]
            except:
                pass
    daemon_dd_calculator.calculate(id, adjancency_matrix)


def create(id):
    global sizes
    if len(sizes) < 3:
        return
    for size in sizes:
        create_topology(id, size)
