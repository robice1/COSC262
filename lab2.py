def sequence_length(n):
    length = 1
    if n == 1:
        return length
    else:
        if n % 2 == 0:
            length += sequence_length(n / 2)
        else:
            length += sequence_length(3 * n + 1)
    return length


def recursive_divide(x, y):
    """performs integer division"""
    if x < y:
        return 0
    else:
        return 1 + recursive_divide(x-y, y)
    
import sys
sys.setrecursionlimit(100000)

def dumbo_func(data, start_index = 0):
    """Takes a list of numbers and does weird stuff with it"""
    if len(data) <= start_index:
        return 0
    else:
        if (data[start_index] // 100) % 3 != 0:
            return 1 + dumbo_func(data, start_index + 1)
        else:
            return dumbo_func(data, start_index + 1)

def my_enumerate(items, start_index = 0):
    """returns a list of tuples (i, item) where item is the ith item"""
    result = []
    if start_index >= len(items):
        return result
    else:
        a_tuple = (start_index, items[start_index])
        result.append(a_tuple)
        result += my_enumerate(items, start_index + 1)
        return result

NUM_RMDS = 9   # number of right-most digits required

def multiply2by2(A, B):
    """Takes two 2-by-2 matrices, A and B, and returns their product. The
    product will only contain a limited number of digits to cope with
    large numbers.  The input and output matrices are in the form of
    lists of lists (of lengths 2). This function only works for 2-by-2
    matrices. The size (dimensions) of the input does not grow with
    respect to n in the original problem. Therefore the time
    complexity of this function is Theta(1). This is different from
    the general matrix multiplication problem where the time
    complexity for multiplying two n-by-n matrices is O(n^3).

    """

    # compute the matrix product
    product = [
        [A[0][0]*B[0][0]+A[0][1]*B[1][0],	A[0][0]*B[0][1]+A[0][1]*B[1][1]],	 
        [A[1][0]*B[0][0]+A[1][1]*B[1][0],	A[1][0]*B[0][1]+A[1][1]*B[1][1]]
        ]
    
    # retain only the required number of digits on the right
    product = [[x % 10**NUM_RMDS for x in row] for row in product]
    
    return product

def matrix_power(A, n):
    """Takes a 2x2 matrix A and a non-negative integer n as exponent and
    returns A raised to the power of n (which will be a 2x2 matrix)."""
    
    # if n is 0 then return the identity matrix.
    if n == 0:
        return [[1, 0],
                [0, 1]]
    power = matrix_power(A, n // 2)
    if n % 2 == 1:
        return multiply2by2(A, multiply2by2(power, power))
    else:
        return multiply2by2(power, power)
    

def fib(n):
    """Returns the n-th Fibonacci number by raising a special matrix to the
    power of n and returning an element on the off-diagonal."""
    
    A = [[1, 1], 
         [1, 0]]
         
    return matrix_power(A, n)[0][1]
