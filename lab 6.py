def counting_sort(iterable, key):
    positions = key_positions(iterable, key)
    return sorted_array(iterable, key, positions)

def key_positions(seq, key):
    k = (max(key(num) for num in seq)) + 1
    C = [0] * k
    for num in seq:
        C[key(num)] += 1
    total = 0
    for i in range(k):
        C[i], total = total, total + C[i]
    return C

def sorted_array(seq, key, positions):
    leng = len(seq)
    B = [0] * leng
    for a in seq:
        B[positions[key(a)]] = a
        positions[key(a)] += 1
    return B

def radix_sort(numbers, d):
    for i in range(d):
        key = lambda n: (n // 10 ** i) % 10
        numbers = counting_sort(numbers, key)
    return numbers
    
