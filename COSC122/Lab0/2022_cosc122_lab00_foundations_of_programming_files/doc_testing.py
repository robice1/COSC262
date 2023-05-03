""" Some fun with doctests
    Quickly scan the module then read through the comments
    in the main code at the bottom
"""
import doctest


def double_word(word):
    """
    Takes a string and returns the string added to itself.
    >>> double_word('blah')
    'blahblah'
    >>> double_word('egg')
    'eggegg'
    >>> double_word('wiggle')
    'wigglewiggle'
    """
    return word *2


def multiply_word(word, n):
    """
    Returns the string n times.
    NOTE: this is currently broken you will need to fix it.
    >>> multiply_word('egg',2)
    'eggegg'
    >>> multiply_word('egg',10)
    'eggeggeggeggeggeggeggeggeggegg'
    """
    return word *n


def has_123(nums):
    """ You should remember this fun function from 121/131 :)
    Returns true if the numbers 1, 2 and 3 appear one after
    the other anywhere in the list of numbers.
    You should be able to write code that passes the tests but isn't completely correct...
    Can you think of some test cases that would catch such erroneous code?
    For example:
    >>> has_123([1, 2, 3])
    True
    >>> has_123([1, 2, 31])
    False
    >>> has_123([4, 3, 1, 2, 3])
    True
    >>> has_123([4, 3, 1, 2, 2])
    False
    >>> has_123([4, 1, 2, 3, 2])
    True
    """
    all_1_idx = (i for i,n in enumerate(nums) if n==1)
    for i in all_1_idx:
        if nums[i:i+3] == [1,2,3]:
            return True
    return False


def lowercase_strings(strings):
    """ Returns a list with all strings converted to lowercase.
    Returns an empty list if strings is empty.

    >>> lowercase_strings(['Right', 'SAID', 'Fred'])
    ['right', 'said', 'fred']
    >>> lowercase_strings(['A', 'BC', 'DEF', 'GHIJ'])
    ['a', 'bc', 'def', 'ghij']
    >>> lowercase_strings(['a', 'bc', 'def'])
    ['a', 'bc', 'def']
    >>> lowercase_strings(['X'])
    ['x']
    >>> lowercase_strings([])
    []
    """
    lowered = []
    for string in strings:
        lowered.append(string.lower())
    return lowered

def evens(numbers):
    """ Takes a list of numbers and returns a list of all the numbers that are even
    >>> evens([1, 2, 3, 4, 5, 6])
    [2, 4, 6]
    >>> evens([1, 3, 5])
    []
    >>> evens([])
    []
    >>> evens([0,2,4])
    [0, 2, 4]
    >>> evens(list(range(1000)))  # doctest: +ELLIPSIS
    [0, 2, 4, 6, ..., 998]
    """
    # Notice that the special ELLIPSIS code tells doctest to allow anything in place
    # of the ... this makes testing large lists a lot nicer :)
    # Write working code for this function using doctests to help you test it.
    even = []
    for num in numbers:
        if num % 2 == 0:
            even.append(num)
    return even


def oh_be_gone(word, n=5):
    """Strips any o characters from the string but only if the
       string has n or more characters (n is 5 characters by
       default).  Simply returns the word if it is shorter than n.
       Remember you can loop over the letters in a string using
       a for loop (or a while loop).
       One way to generate the result is to build a result string
       by adding all the valid letters as you loop through the original.
       For example:
    >>> oh_be_gone("Algo")
    'Algo'
    >>> oh_be_gone("Borat")
    'Brat'
    >>> oh_be_gone("beon", 3)
    'ben'
    >>> oh_be_gone("bon", 2)
    'bn'
    >>> oh_be_gone("on", 2)
    'n'
    >>> oh_be_gone("on", 3)
    'on'
    >>> oh_be_gone("oh my what is going on", 10)
    'h my what is ging n'
    """
    if len(word) > n-1:
        word = word.replace('o', '')
    return word


def same_ends(string_1, string_2):
    """ Takes two non-empty string parameters string_1 and string_2 and returns True if string_1
    and string_2 both start with the same character and both end with the same character
    except if string_1 is equal to string_2 in which case the function returns False.
    In all other cases the function returns False.
    Remember you can index into a string to get specific characters,
       eg, my_string[0] will return the first letter in a string.
    Write doctests here to test your code for this function!!!
    >>> same_ends('long ballz', 'large ballz')
    True
    >>> same_ends('these', 'that')
    False
    >>> same_ends('this', 'this')
    False
    """
    if string_1 != string_2:
        if string_1[0] == string_2[0]:
            if string_1[-1] == string_2[-1]:
                return True
    return False

if __name__ == '__main__':

    # run single tests
    # each will print nothing if there are no errors
    # uncomment each test you want to run
    # globs=None sets the global variables used in the tests to None
    # you don't need to know why, you just need to do it...
    doctest.run_docstring_examples(double_word, globs=None)
    # the next test will initially fail - you should fix the code

    doctest.run_docstring_examples(multiply_word, globs=None)

    # Complete the functions below so that they pass the tests
    # Remember passing the tests doesn't necessaryily mean that
    # your code works in all cases - it just works for those tested!
    doctest.run_docstring_examples(has_123, globs=None)
    doctest.run_docstring_examples(lowercase_strings, globs=None)
    doctest.run_docstring_examples(evens, globs=None)
    doctest.run_docstring_examples(oh_be_gone, globs=None)
    doctest.run_docstring_examples(same_ends, globs=None)

    # run all tests
    # To run all tests simply comment out the single tests above
    # and uncomment the two lines below :)
    # This has the benefit of being able to print the test results
    test_results = doctest.testmod()
    print(test_results)
