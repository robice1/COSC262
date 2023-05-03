""" Doctests are fun """
import doctest

def triple(n):
    """ Returns triple n, ie, 3*n
    >>> triple(1)
    3
    >>> triple(10)
    30
    >>> triple('wow')
    'wowwowwow'
    >>> triple('deez')
    'deezdeezdeez'
    """
    return 3 * n


doctest.testmod()