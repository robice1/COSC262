def adjacency_list(graph_str):
    """takes the textual rep of a graph and returns it as an adjacency list"""
    lines = graph_str.splitlines()
    header = lines[0].split()
    directed = header[0] == 'D'
    num_vertices = int(header[1])
    weighted = len(header) == 3 and header[2] == 'W'
    adj_list = [[] for i in range(num_vertices)]
    for line in lines[1:]:
        vertices = line.split()
        node = int(vertices[0])
        dest = [int(num) for num in vertices[1:]]
        if weighted is True:
            edges = [(dest[i], int(dest[i+1])) for i in range(0, len(dest), 2)]
        else:
            edges = [(destination, None) for destination in dest]
        for destination, weight in edges:
            if directed is True:
                adj_list[node].append((destination, weight))
            else:
                adj_list[node].append((destination, weight))
                adj_list[destination].append((node, weight))
    return adj_list

def adjacency_matrix(graph_str):
    """returns the adjacency matrix of a graph from it's textual rep"""
    lines = graph_str.splitlines()
    header = lines[0].split()
    directed = header[0] == 'D'
    num_vertices = int(header[1])
    weighted = len(header) == 3 and header[2] == 'W'
    adj_matrix = [[None] * num_vertices for i in range(num_vertices)]
    for line in lines[1:]:
        vertices = line.split()
        node, dest = int(vertices[0]), int(vertices[1])
        weight = 1 if not weighted else int(vertices[2])
        adj_matrix[node][dest] = weight
        if directed is not True:
            adj_matrix[dest][node] = weight
    if not weighted:
        for i in range(num_vertices):
            for j in range(num_vertices):
                if adj_matrix[i][j] == None:
                    adj_matrix[i][j] = 0
    return adj_matrix


from collections import deque


def bfs_tree(adj_list, start):
    n = len(adj_list)
    state = [0] * n
    parent = [None] * n
    q = deque()
    state[start] = 1
    q.append(start)
    while q:
        u = q.popleft()
        for v, edge in adj_list[u]:
            if state[v] == 0:
                state[v] = 1
                parent[v] = u
                q.append(v)
        state[u] = -1
    return parent

graph_str = """\
U 6
0 4
5 4
4 2
2 3
3 0
3 4"""
adj_list = adjacency_list(graph_str)
print(bfs_tree(adj_list, 5))

def dfs_tree(adj_list, start):
    n = len(adj_list)
    state = [0] * n # 0 = undiscovered, 1 = discovered, -1 = processed
    parent = [None] * n
    state[start] = 1
    def dfs_loop(adj_list, u, state, parent):
        for v, edge in adj_list[u]:
            if state[v] == 0:
                state[v] = 1
                parent[v] = u
                dfs_loop(adj_list, v, state, parent)
            state[u] = -1
    dfs_loop(adj_list, start, state, parent)
    return parent

# an undirected graph

adj_list = [
    [(1, None), (2, None)],
    [(0, None), (2, None)],
    [(0, None), (1, None)]
]

print(dfs_tree(adj_list, 0))
print(dfs_tree(adj_list, 1))
print(dfs_tree(adj_list, 2))