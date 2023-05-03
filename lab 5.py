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

from math import inf

def distance_matrix(adj_list):
    n = len(adj_list)
    distances = [[0 if i==j else float('inf') for j in range(n)] for i in range(n)]
    for i in range(n):
        for vertex, weight in adj_list[i]:
            distances[i][vertex] = weight
    return distances


def floyd(distance):
    n = len(distance)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distance[i][j] > distance[i][k] + distance[k][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
    return distance


def all_paths(adj_list, source, destination):
    paths = []
    dfs_backtrack((source,), destination, adj_list, paths)
    return paths

def permutations(s):
    solutions = []
    dfs_backtrack((), s, solutions)
    return solutions


def dfs_backtrack(candidate_path, destination, adj_list, output_data):
    if is_solution(candidate_path, destination):
        add_to_output(candidate_path, output_data)
    else:
        for child_candidate in children(candidate_path, adj_list):
            dfs_backtrack(child_candidate, destination, adj_list, output_data)

    
def add_to_output(candidate, output_data):
    output_data.append(candidate)

    
def should_prune(candidate):
    return False

def is_solution(candidate_path, destination):
    """Returns true if the candidate is a complete solution"""
    return candidate_path[-1] == destination

def children(candidate_path, adj_list):
    """returns a collection of candidates that are the children of the given candidate"""
    current_vertex = candidate_path[-1]
    children = []
    for neighbour, edge in adj_list[current_vertex]:
        if neighbour not in candidate_path:
            children.append(candidate_path + (neighbour,))
    return children

from pprint import pprint

# graph used in tracing bfs and dfs
graph_str = """\
D 7
6 0
6 5
0 1
0 2
1 2
1 3
2 4
2 5
4 3
5 4
"""

adj_list = adjacency_list(graph_str)
pprint(sorted(all_paths(adj_list, 6, 3)))