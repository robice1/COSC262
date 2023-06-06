import sys

sys.setrecursionlimit(2000)

class Item:
    """An item to (maybe) put in a knapsack. Weight must be an int."""
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __repr__(self):
        """The representation of an item"""
        return f"Item({self.value}, {self.weight})"
        

def max_value1(items, capacity):
    """Top down version"""
    n = len(items)
    cache = [[float('inf')] * (capacity + 1) for x in range(n+1)]
    def top_down(n, capacity):
        if n == 0 or capacity == 0:
            return 0
        if cache[n][capacity] != float('inf'):
            return cache[n][capacity]
        if items[n-1].weight > capacity:
            result = top_down(n-1, capacity)
        else:
            include_item = items[n-1].value + top_down(n-1, capacity - items[n-1].weight)
            exclude_item = top_down(n-1, capacity)
            result = max(include_item, exclude_item)
        cache[n][capacity] = result
        return result
    return top_down(n, capacity)

def max_value(items, capacity):
    n = len(items)
    cache = [[0] * (capacity + 1) for x in range(n+1)]
    for i in range(1, n + 1):
        for j in range(1, capacity+1):
            item_weight = items[i-1].weight
            item_value = items[i-1].value
            if item_weight > j:
                cache[i][j] = cache[i-1][j]
            else:
                cache[i][j] = max(cache[i - 1][j], item_value + cache[i - 1][j - item_weight])
    items_added = []
    i, j = n, capacity
    while i > 0 and j > 0:
        if cache[i][j] != cache[i-1][j]:
            items_added.append(items[i-1])
            j -= items[i-1].weight
        i -= 1
    return cache[n][capacity], items_added

def lcs(s1, s2):
    cache = {}
    def top_down(s1, s2):
        if (s1, s2) in cache:
            return cache[(s1, s2)]
    
        if s1 == '' or s2 == '':
            result = ''
        elif s1[0] == s2[0]:
            result = s1[0] + top_down(s1[1:], s2[1:])
        else:
            soln1 = top_down(s1[1:], s2)
            soln2 = top_down(s1, s2[1:])
            if len(soln1) > len(soln2):
                result = soln1
            else:
                result = soln2
        cache[(s1, s2)] = result
        return result
    return top_down(s1, s2)

def edit_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill DP table bottom-up
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i * 2
            else:
                cost = 0 if s1[i - 1] == s2[j - 1] else 4
                dp[i][j] = min(dp[i-1][j] + 2, dp[i][j-1] + 1, dp[i-1][j-1] + cost)

    return dp

print(edit_distance('them', 'tim'))