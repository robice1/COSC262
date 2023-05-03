""" Try to predict what these functions
    will do before running them...
"""


def count(val):
    """ Predict what I'll do before you run me """
    if val <= 0:
        print(val)
    else:
        print(val)
        count(val -1)


def recount(val):
    """ Predict what I'll do before you run me """
    if val <= 0:
        print(val)
    else:
        recount(val -1)
        print(val)


def boggle(val):
    """ Predict what I'll do before you run me """
    if val <= 0:
        print(val)
    else:
        boggle(val -1)
        print(val)
        boggle(val -1)

def zingle(val):
    """ You should do this by hand - you'll have to in the test/exam! """
    if val <= 1:
        print(val)
    else:
        print(val)
        zingle(val-1)
        print(val)

def num_lines_output(n):
    """ Returns the number of lines of output printed
    by the recursive boggle function for a given value of n.
    Note: this is simply the recurrence relation for
    the number of lines, written in python.
    """
    if n <= 0:
        return 1  
    else:
        return 1 + 2*num_lines_output(n-1)
    
def num_of_adds(n):
    """ Returns the number of adds used by the recursive 
    fibonacci calculation function for a given n.
    Note: this is simply the recurrence relation for
    the number of adds, written in python.
    """
    if n <= 2:
        return 0  
    else:
        return 1 + num_of_adds(n-1) + num_of_adds(n-2)
    
print(num_of_adds(7))