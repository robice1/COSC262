def change_greedy(amount, coinage):
    """takes an integer amount of money in some units plus a list of integer 
    coin values and returns the breakdown of that amount of coins (greedy)"""
    coinage.sort(reverse=True)
    coins_used = []
    for coin in coinage:
        while amount > 0:
            if coin <= amount:
                coins_used.append(coin)
                amount -= coin
            else:
                break
    breakdown = []
    if amount == 0:
        for coin in sorted(set(coins_used), reverse=True):
            n = coins_used.count(coin)
            breakdown.append((n, coin))
        return breakdown
    else:
        return None

def print_shows(show_list):
    show_list.sort(key=lambda x: x[1] + x[2])
    s = []
    t_current = 0
    for i in range(len(show_list)):
        if show_list[i][1] >= t_current:
            s.append(show_list[i])
            t_current = show_list[i][2] + show_list[i][1]
    for show in s:
        print(f"{show[0]} {show[1]} {show[2] + show[1]}")

shows = ([
    ('a', 0, 6),
    ('b', 1, 3),
    ('c', 3, 2),
    ('d', 3, 5),
    ('e', 4, 3),
    ('f', 5, 4),
    ('g', 6, 4), 
    ('h', 8, 3)])

shows.sort(key = lambda x: x[1] + x[2])

print_shows(shows)