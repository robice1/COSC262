def smallest_factorial(target):
    """Returns the smallest value of n such that n! is greater than or equal 
    to the target"""
    i = 0
    fact = 1
    while (fact < target):
        i += 1
        fact = fact * i
    return(i)
        

print(smallest_factorial(2))
print(smallest_factorial(10000))