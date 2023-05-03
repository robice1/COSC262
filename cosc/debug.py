def num_halvings(num_sheets_of_paper):
    """Return the number of times the given number of sheets of paper
       can be halved before the result becomes zero. For example, if n == 12
       the sequence of halvings would be 12, 6, 3, 1, 0 and the function
       would return 4, since the 4th halving yielded zero.
    """
    n = num_sheets_of_paper
    halvings = 0 # Counter of the number of halvings
    while n > 0:
        halvings += 1
        n = n // 2
    return halvings
print(num_halvings(64))