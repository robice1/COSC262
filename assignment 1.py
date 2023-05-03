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

from collections import deque

def bfs_tree(adj_list, start):
    n = len(adj_list)
    state = [0] * n # 0 = undiscovered, 1 = discovered, -1 = processed
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
    return parent, state

def format_sequence(converters_info, source_format, destination_format):
    adj_list = adjacency_list(converters_info)
    parent = bfs_tree(adj_list, source_format)
    def tree_path(parent, s, t):
        result = []
        if s == t:
            result.append(s)
            return result
        else:
            if parent[t] == None:
                return False
            else:
                result += tree_path(parent, s, parent[t])            
                result.append(t)
                return result
    result = tree_path(parent, source_format, destination_format)
    if not result:
        return "No solution!"
    else:
        return result
    
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
    return state


def bubbles(physical_contact_info):
    """Takes information about physical contact and returns the bubbles"""
    adj_list = adjacency_list(physical_contact_info)
    bubbles = []
    visited = set()
    for i in range(len(adj_list)):
        if i not in visited:
            visited.add(i)
            state = dfs_tree(adj_list, i)
            bubble = []
            for v in range(len(state)):
                if state[v] == -1:
                    visited.add(v)
                    bubble.append(v)
            bubbles.append(bubble)
    return bubbles

from collections import deque

def build_order(dependencies):
    adj_list = adjacency_list(dependencies)
    n = len(adj_list)
    state = [0] * n # undiscovered 0, discovered 1, processed -1
    parent = [None] * n
    stack = deque([])
    def dfs_loop(adj_list, u, state, parent, stack):
        for v, edge in adj_list[u]:
            if state[v] == 0:
                state[v] = 1
                parent[v] = u
                dfs_loop(adj_list, v, state, parent, stack)
        state[u] = -1
        stack.appendleft(u)
    for i in range(len(adj_list)):
        if state[i] == 0:
            dfs_loop(adj_list, i, state, parent, stack)
    topo_order = []
    for i in range(len(stack)):
        topo_order.append(stack.popleft())
    return topo_order

from math import inf, ceil

def next_vertex(in_tree, distance):
    min_dist = float('inf')
    next_vert = None
    for i in range(len(in_tree)):
        if not in_tree[i] and distance[i] <= min_dist:
            min_dist = distance[i]
            next_vert = i
    return next_vert

def which_segments(city_map):
    adj_list = adjacency_list(city_map)
    n = len(adj_list)
    in_tree = [False] * n
    distance = [float('inf')] * n
    parent = [None] * n
    distance[0] = 0
    while not all(in_tree):
        u = next_vertex(in_tree, distance)
        in_tree[u] = True
        for v, weight in adj_list[u]:
            if not in_tree[v] and weight < distance[v]:
                distance[v] = weight
                parent[v] = u
    mst = []
    for i in range(len(parent)):
        if parent[i] is not None:
            if i <= parent[i]:
                segment = (i, parent[i])
            else:
                segment = (parent[i], i)
            mst.append(segment)
    return mst

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

def min_capacity(city_map, depot_position):
    adj_list = adjacency_list(city_map)
    parent, distance = dijkstra(adj_list, depot_position)
    efficiency = 3 / 2 # 3 units of battery per 2 units distance
    reachables = [x for x in distance if x != float('inf')]
    furthest = max(reachables)
    return_dist = furthest * 2
    min_charge = 2 * return_dist
    return ceil(min_charge)

city_map = """\
U 4 W
0 2 5
0 3 2
3 2 2
"""

print(min_capacity(city_map, 0))
print(min_capacity(city_map, 1))
print(min_capacity(city_map, 2))
print(min_capacity(city_map, 3))