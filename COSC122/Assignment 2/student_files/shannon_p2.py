"""
An improved program that plays Shannon's Game.
Students should enter their name and number below!

Work developed during COSC122-22SU2 by:

Tutor Author: Liam Laing
Email: liam.laing@canterbury.ac.nz

Student Author: Robert Ivill
Email: riv14@uclive.ac.nz
"""

import re
import time
import sys
from unicodedata import category

CORPUS_DIR = "data"
DEFAULT_CORPUS = 'corpus.txt'


def _c_mul(num_a, num_b):
    '''Substitute for c multiply function'''
    return (int(num_a) * int(num_b)) & 0xFFFFFFFF


def nice_hash(input_string):
    """ Takes a string name and returns a hash for the string. This hash value
    will be os independent, unlike the default Python hash function.
    It will also be stable across runs of Python, unlike the default.
    """
    if input_string is None:
        return 0  # empty
    value = ord(input_string[0]) << 7
    for char in input_string:
        value = _c_mul(1000003, value) ^ ord(char)
    value = value ^ len(input_string)
    if value == -1:
        value = -2
    return value


class Frequency():
    """
    DO NOT MODIFY THIS CLASS.
    Stores a letter:frequency pair.
    The repr for printing will be of the form (item, frequency)
    """

    def __init__(self, item, frequency):
        self.item = item
        self.frequency = frequency
        self.next_node = None

    def __repr__(self):
        return f'({repr(self.item)}, {repr(self.frequency)})'


class SortedFrequencyList():
    """
    Stores a collection of Frequency objects as a sorted linked list.
    Items are sorted from the highest frequency to the lowest.
    """

    def __init__(self):
        self.head = None

    def add(self, item, frequency=1):
        """
        Adds the given letter and frequency combination as a Frequency object
        to the list. If the given letter is already in the list, the given
        frequency is added to its frequency.

        If the updated frequency is greater than the frequency of the previous
        node then it should be moved into order, ie, so that it is after
        all items with the same or greater frequency.

        If the letter is not in the list then the new frequency object should be
        added to the list so that it is after all letters
        with the same or higher frequency.

        Adding new letters with frequency 1 should be the sole usage case in
        this assignment and you can make your code more efficient if you treat
        letters with frequency of 1 as a special case. But, your code should
        still deal with the more general case, eg, my_list.add('a', 4)

        Of course, if there are no letters in the list
        then the new item should be added at the head.

        The example below should make it clear how this method should work.
        Hint: you should have code similar to this in your answers to lab 3 :)

        You will probably want to use a helper function.
        >>> f = SortedFrequencyList()
        >>> f.add('a', 1)
        >>> f
        ('a', 1) ->
        >>> f.add('b', 1)
        >>> f
        ('a', 1) -> ('b', 1) ->
        >>> f.add('c', 1)
        >>> f
        ('a', 1) -> ('b', 1) -> ('c', 1) ->
        >>> f.add('c', 1)
        >>> f
        ('c', 2) -> ('a', 1) -> ('b', 1) ->
        >>> f.add('b', 1)
        >>> f
        ('c', 2) -> ('b', 2) -> ('a', 1) ->
        """
        # ---start student section---
        in_list = self.__contains__(item)
        current = self.head
        if in_list is False:
            new_node = Frequency(item, frequency)
            if current is None:
                self.head = new_node
                self.head.next_node = None
            else:
                while current.next_node is not None:
                    current = current.next_node
                current.next_node = new_node
        else:
            if current.item == item:
                current.frequency += frequency
            else:
                while current.next_node.item != item:
                    current = current.next_node
                current.next_node.frequency += frequency
                add_node = current.next_node
                current.next_node = add_node.next_node
                if add_node.frequency > self.head.frequency:
                    add_node.next_node = self.head
                    self.head = add_node
                else:
                    current_2 = self.head
                    while (current_2.next_node is not None and 
                           add_node.frequency <= current_2.next_node.frequency):
                        current_2 = current_2.next_node
                    add_node.next_node = current_2.next_node
                    current_2.next_node = add_node
                    
        # ===end student section===

    def remove(self, item):
        """
        Removes the Frequency object with the given `item` from the list.
        Does nothing if `item` is not in the list.
        """
        # ---start student section---
        current = self.head
        if current is not None:
            if current.item == item:
                self.head = current.next_node
                current = None
        while current is not None:
            if current.item == item:
                break
            prev = current
            current = current.next_node
        if current is None:
            return
        prev.next_node = current.next_node
        current = None        
        # ===end student section===

    def find(self, item):
        """
        Returns the Frequency object for the given `item` in the list, or
        None if the `item` doesn't appear in the list.
        """
        # ---start student section---
        current = self.head
        while current is not None:
            if current.item == item:
                return current
            current = current.next_node
        return None        
        # ===end student section===

    def __contains__(self, item):
        # you should use the find method here
        # ---start student section---
        return self.find(item) is not None
        # ===end student section===

    def __iter__(self):
        """ Note this will be used to return a simple list of Frequency items
        eg, list(my_sorted_frequency_list)
        Students shouldn't change this method and don't need to understand it.
        """
        current = self.head
        while current is not None:
            yield current.item
            current = current.next_node

    def __repr__(self):
        """ Returns a string representation of the list, eg, SFL(<'e': 2>, <'d': 1>))
        """
        result = ''
        current = self.head
        while current is not None:
            result += repr(current) + ' -> '
            current = current.next_node
        return result.strip()


class PrefixItem():
    """
    DO NOT MODIFY THIS CLASS.
    Stores a prefix:possibles pair.
    """

    def __init__(self, prefix, possibles):
        """
        Initialises a new PrefixItem with the given letter `prefix` and
        SortedFrequencyList of `possibles`.
        """
        self.prefix = prefix
        self.possibles = possibles

    def __hash__(self):
        return nice_hash(self.prefix)

    def __repr__(self):
        return f'{repr(self.prefix):5}: {repr(self.possibles)}'


class PrefixTable():
    """
    A simple hash table for storing prefix:possible combinations using
    PrefixItems internally.
    """

    def __init__(self, slots):
        """
        Initialises the PrefixTable with a number of `slots`. The table cannot
        store more items than the number of slots specified here.
        """
        self.data = [None] * slots
        self.n_slots = slots
        self.n_items = 0

    def store(self, prefix, possibles):
        """
        Stores the given letter `prefix` and list of `possibles` (a
        SortedFrequencyList) in the hash table using a PrefixItem. If the
        item is successfully stored in the table, this method returns
        True, otherwise (for example, if there is no more room left in the
        table) it returns False.
        Make sure you use nice_hash to get the initial hash
        and remember you are using linear probing for clashes.
        """
        # ---start student section---
        item = PrefixItem(prefix, possibles)
        hash_no = nice_hash(prefix)
        index = hash_no % self.n_slots
        if self.n_slots == self.n_items:
            return False
        else:
            while self.data[index] is not None:
                if index >= self.n_slots - 1:
                    index = 0
                else:
                    index += 1
            self.data[index] = item
            self.n_items += 1
            return True
        # ===end student section===

    def fetch(self, prefix):
        """"
        Returns the SortedFrequencyList of possibles associated with the given
        letter `prefix', or None if the `prefix` isn't stored in the table.
        Make sure you use nice_hash to get the initial hash
        and remember you are using linear probing for clashes
        """
        # ---start student section---
        hash_no = nice_hash(prefix)
        first_index = hash_no % self.n_slots
        if not self.__contains__(prefix):
            return None
        else:
            i = 0
            current_index = (first_index + i) % self.n_slots
            while (self.data[current_index] is not None and 
                   self.data[current_index].prefix != prefix):
                i += 1
                current_index = (first_index + i) % self.n_slots
            return self.data[current_index].possibles
        # ===end student section===

    def __contains__(self, prefix):
        """ Returns True if prefix is in the table, otherwise False"""
        # ---start student section---
        hash_no = nice_hash(prefix)
        first_hash = hash_no % self.n_slots        
        found = False
        # check item at initial slot
        if (self.data[first_hash] is not None and 
            self.data[first_hash].prefix == prefix):
            found = True
        else:
            i = 1
            current_index = (first_hash + i) % self.n_slots
            while self.data[current_index] is not None and not found:
                if current_index == first_hash:
                    # back to original hash and didn't find item
                    # so give up
                    # phew - the hashtable is full!
                    break
                if self.data[current_index].prefix == prefix:
                    # horay we found it
                    found = True
                else:
                    # try next slot
                    i += 1
                    current_index = (first_hash + i) % self.n_slots
        return found
        # ===end student section===

    def __repr__(self):
        ans = ""
        i = 0
        count = 0
        skipping = False
        while i < len(self.data):
            item = self.data[i]
            if item is None:
                count += 1
                if count >= 3 and not skipping and i < len(
                        self.data) - 1 and self.data[i + 1] is None:
                    skipping = True
                    ans += '...\n'
            else:
                skipping = False
                count = 0

            if not skipping:
                ans += f'{i:>4} {repr(item)}\n'
            i += 1
        return ans.rstrip()


def process_corpus(corpus, unique_chars):
    """
    Returns a PrefixTable populated with the possible characters that follow
    each character pair in `corpus`. `unique_chars` is the number of unique
    characters in `corpus`.

    The size of the PrefixTable should be chosen by calculating the maximum
    number of character pairs (the square of `unique_chars`). In practice,
    the actual number of unique paris in the corpus will be considerably less
    than this, so we are guaranteed a low load factor.

    WARNING: Clashes may still occur and you must use linear probing
    to resolve clashes
    """
    # ---start student section---
    num_slots = unique_chars ** 2
    guess_table = PrefixTable(num_slots)
    char_pairs = []
    lowercase_corp = corpus.lower()
    corpus_list = []
    corpus_list[:0] = lowercase_corp
    for i in range(len(corpus_list)-2):
        char_pairs.append(corpus_list[i] + corpus_list[i+1])
    unique_pairs = []
    for item in char_pairs:
        if item not in unique_pairs:
            unique_pairs.append(item)
    char_pairs = list(unique_pairs)
    for pair in char_pairs:
        possibles = []
        for i in range(len(lowercase_corp) - 2):
            if lowercase_corp[i:i+2] == pair:
                possibles.append(lowercase_corp[i+2])
        frequencies = SortedFrequencyList()
        for item in possibles:
            frequencies.add(item)
        guess_table.store(pair, frequencies)
    return guess_table
    # ===end student section===


def run_time_trials():
    """ A good place to write code for time trials
    Make sure you use this docstring to explain your code and that
    you write comments in your code to help explain the process.
    """
    

def run_some_trials():
    """ Play some games with various test phrases and settings """
    # play game using whatever you like
    # maybe put an input statement here
    # so you can enter the corpus
    # and settings
    # or just run various games with various settings

    test_phrases = ['jaaugftvfjcyzzmxyosavusezfkfytnlabmnraqybna']

    ## 'Hello isn\'t it a lovely day today.']
    ## MAKE SURE you test with various phrases!

    test_files = [f'{CORPUS_DIR}/war-and-peace.txt'
                  ]

    # Uncomment the block below to run trials based on the lists of phrases and files above
    for test_phrase in test_phrases:
        for corpus_filename in test_files:
            phrase_length = 0   # for auto-run
            load_corpus_and_play(corpus_filename, test_phrase, phrase_length)
            print('\n'*3)

    # check out https://www.gutenberg.org/ for more free books!

    # interactive trial
    # see how long the program takes to guess 'bat man'
    # it will get the first two characters and start asking you
    # if it has the third character correct etc...
    # load_corpus_and_play(corpus_filename, 'ba', 7)


###############################################################################
################# DO NOT MODIFY ANYTHING INSIDE THE BLOCK BELOW ###############
################## YOU MUST INCLUDE THIS CODE IN YOUR SUBMISSION ##############
###############################################################################
################# There is some code below this block you should read #########
###############################################################################

def fallback_guesses(possibles):
    """
    Returns all characters from a--z, and some punctuation that don't appear in
    `possibles`.
    """
    all_fallbacks = [chr(c) for c in range(ord('a'), ord('z') + 1)] + \
                    [' ', ',', '.', "'", '"', ';', '?', '!']
    return [x for x in all_fallbacks if x not in possibles]


def format_document(doc):
    """
    Re-formats `d` by collapsing all whitespace characters into a space and
    stripping all characters that aren't letters or punctuation.
    """
    # http://www.unicode.org/reports/tr44/#General_Category_Values
    allowed_types = ('Lu', 'Ll', 'Lo', 'Po', 'Zs')
    # Collapse whitespace
    doc = re.compile(r'\s+', re.UNICODE).sub(' ', doc)
    doc = u''.join([cat.lower()
                    for cat in doc if category(cat) in allowed_types])
    # Remove .encode() to properly process a unicode corpus
    return doc


def confirm(prompt):
    """
    Asks the user to confirm a yes/no question.
    Returns True/False based on their answer.
    """
    answer = ' '
    while len(answer) == 0 or answer[0].lower() not in ('y', 'n'):
        answer = input(prompt + ' (y/n) ')
    return answer[0].lower() == 'y'


def check_guess(next_char, guess):
    """
    Returns True if `guess` matches `next_char`, or asks the user if
    `next_char` is None.
    """
    if next_char is not None:
        return next_char == guess
    else:
        return confirm(f" '{guess}'?")


def next_guess(guesses):
    """ Returns the next guess """
    return guesses.pop(0) if len(guesses) else None


def check_guesses(next_char, guesses):
    """
    Runs through `guesses` to check against `next_char` (or asks the user if
    `next_char` is None).
    If a correct guess is found, (guess, count) is returned; otherwise
    (None, count) is returned. Where `count` is the number of guesses
    attempted.
    """
    guess = next_guess(guesses)
    guess_count = 0
    while guess is not None:
        guess_count += 1
        if check_guess(next_char, guess):
            return (guess, guess_count)
        guess = next_guess(guesses)
    # Wasn't able to find a guess
    return (None, guess_count)


def guess_next_char(phrase, progress, table, is_auto):
    """ Takes the full phrase, the progress string, the hash table
    and the is_auto flag and returns the next character once it has
    been guessed successfully. Also returns the number of guesses
    used in this guessing.
    """
    # Figure out what the next character to guess is
    # set it to None if not doing auto
    next_char = phrase[len(progress)].lower() if is_auto else None

    # Find possible guesses
    last_two_chars = progress[-2:].lower()
    guesses = table.fetch(last_two_chars)
    if guesses is None:
        guesses = []
    # Convert guesses into a list
    guesses = list(guesses)

    fallbacks = fallback_guesses(guesses)
    fallbacks = list(fallbacks)

    # Try to guess it from the table
    (guess, guess_count) = check_guesses(next_char, guesses)

    if guess is None:
        # If guessing from the corpus failed, try to guess from the
        # fallbacks
        (guess, current_guess_count) = check_guesses(next_char, fallbacks)
        if guess is None:
            # If that failed, we're screwed!
            print(' Exhaused all fallbacks! Failed to guess phrase.')
            # Give up and exit the program
            sys.exit(1)
        guess_count += current_guess_count
    return guess, guess_count


def play_game(table, phrase, phrase_len=0):
    """
    Plays the game.
      `table` is the table mapping keys to lists of character frequencies.
      `phrase` is the phrase to match, or part of the phrase.
      `phrase_len` is the total length of the phrase or 0 for auto mode
    If `phrase_len` is zero, then the game is played automatically and
    the phrase is treated as the whole phrase. Otherwise the phrase is
    the start of the phrase and the function will ask the user whether
    or not it's guesses are correct - and keep going until phrase_len
    characters have been guessed correctly.

    Given phrase_len is 0 by default leaving out phrase_len from
    calls will auto-run, eg, play_game(table, 'eggs') will auto-run

    Returns the total number of guesses taken and the total time taken
    If in interactive mode the time taken value will be 0.
    """
    start = time.perf_counter()
    # Play the game automatically if phrase_len is 0
    is_auto = phrase_len == 0

    # Set phrase length to length of supplied phrase
    if is_auto:
        phrase_len = len(phrase)

    progress = phrase[0:2]
    gap_line = '_' * (phrase_len - len(progress))
    total_guesses = 0
    print(f'{progress}{gap_line}  {0:02}')
    while len(progress) < phrase_len:
        guess, count = guess_next_char(phrase, progress, table, is_auto)
        progress += guess
        total_guesses += count
        # Print current progress and guess count for the last letter
        gap_line = '_' * (phrase_len - len(progress))
        print(f'{progress}{gap_line}  {count:02}')
    end = time.perf_counter()
    print(' Solved it in {} guesses!'.format(total_guesses))

    # return zero time taken if in interactive mode
    time_taken = end - start if is_auto else 0

    return total_guesses, time_taken


def load_corpus_and_play(corpus_filename, phrase, length=0):
    """ Loads the corpus file and plays the game with the given setttings """
    with open(corpus_filename) as infile:
        corpus = format_document(infile.read())
        unique_chars = len(set(corpus))
        slice_of_corpus = corpus[0:1000] 
        table = process_corpus(slice_of_corpus, unique_chars)
        _, time_taken = play_game(table, phrase, length)
        if length == 0:
            print('Took {:0.6f} seconds'.format(time_taken))


###############################################################################
#################### DO NOT MODIFY ANYTHING INSIDE THE BLOCK ABOVE ############
############ YOU MUST STILL INCLUDE THE BLOCK ABOVE IN YOUR SUBMISSION ########
###############################################################################


# IMPORTANT - Read all the comments below!!!
# ---------


#def random_string(size):
    #"""Remove me before submission, I might be helpful in for answering the
    #short answer questions"""
    #from random import randint
    #return "".join(
        #chr(ord('a') + randint(0, 25)) for _ in range(size)
    #)


def main():
    """put any code testing things in here, or in a unit test."""
    run_some_trials()


    # run this code if not being imported
if __name__ == '__main__':
    main()

