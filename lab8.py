"""A program to read a grid of weights from a file and compute the 
   minimum cost of a path from the top row to the bottom row
   with the constraint that each step in the path must be directly
   or diagonally downwards. 
   This question has a large(ish) 200 x 200 grid and you are required
   to use a bottom-up DP approach to solve it.
"""
INFINITY = float('inf')  

def read_grid(filename):
    """Read from the given file an n x m grid of integer weights.
       The file must consist of n lines of m space-separated integers.
       n and m are inferred from the file contents.
       Returns the grid as an n element list of m element lists.
       THIS FUNCTION DOES NOT HAVE BUGS.
    """
    with open(filename) as infile:
        lines = infile.read().splitlines()

    grid = [[int(bit) for bit in line.split()] for line in lines]
    return grid


def grid_cost(grid):
    """The cheapest cost from row 1 to row n (1-origin) in the given grid of
       integer weights.
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    costs_grid = [[0 for n in range(n_cols)] for n in range(n_rows)]
    for j in range(n_cols):
        costs_grid[0][j] = grid[0][j]
    for i in range(1, n_rows):
        for j in range(n_cols):
            left = costs_grid[i-1][j-1] if j > 0 else INFINITY
            middle = costs_grid[i-1][j]
            right = costs_grid[i-1][j+1] if j <= n_cols else INFINITY
            costs_grid[i][j] = grid[i][j] + min(left, right, middle)
    best = min(costs_grid[n_rows - 1])
    return best
    
    
def file_cost(filename):
    """The cheapest cost from row 1 to row n (1-origin) in the grid of integer
       weights read from the given file
    """
    return grid_cost(read_grid(filename))


def coins_reqd(value, coinage):
    """A version that doesn't use a list comprehension"""
    num_coins = [0] * (value + 1)
    predecessor = [None] * (value + 1)
    for amt in range(1, value + 1):
        minimum = INFINITY
        for c in coinage:
            if c <= amt:
                coin_count = num_coins[amt - c]  # Num coins required to solve for amt - c
                if minimum is None or coin_count < minimum:
                    minimum = coin_count
                    predecessor[amt] = c
        num_coins[amt] = 1 + minimum
    coins_used = []
    amt = value
    while amt > 0:
        c = predecessor[amt]
        coins_used.append(c)
        amt -= c
    coinage = [(c, coins_used.count(c)) for c in sorted(set(coins_used), reverse=True)]
    return coinage
coinage = [1, 10, 25]
amount = 32
coinage_copy = coinage[:]
answer = coins_reqd(amount, coinage)
print(answer)