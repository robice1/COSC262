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

def transpose(adj_list):
    n = len(adj_list)
    transpose = [[] for i in range(n)]
    for u in range(n):
        for v, w in adj_list[u]:
            transpose[v].append((u, w))
    return transpose

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
    return parent, state

def is_strongly_connected(adj_list):
    parent, state = dfs_tree(adj_list, 0)
    for x in state:
        if x == 0:
            return False
    tgraph = transpose(adj_list)
    tparent, tstate = dfs_tree(tgraph, 0)
    for x in tstate:
        if x == 0:
            return False
    return True
    
def next_vertex(in_tree, distance):
    min_dist = float('inf')
    next_vert = None
    for i in range(len(in_tree)):
        if not in_tree[i] and distance[i] <= min_dist:
            min_dist = distance[i]
            next_vert = i
    return next_vert

from math import inf

def dijkstra(adj_list, start):
    n = len(adj_list)
    in_tree = [False] * n
    distance = [float('inf')] * n
    parent = [None] * n
    distance[start] = 0
    while not all(in_tree):
        u = next_vertex(in_tree, distance)
        in_tree[u] = True
        for v, weight in adj_list[u]:
            if not in_tree[v] and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                parent[v] = u
    return parent, distance

graph_string = """\
D 3 W
1 0 3
2 0 1
1 2 1
"""

print(dijkstra(adjacency_list(graph_string), 1))
print(dijkstra(adjacency_list(graph_string), 2))