"""
A simple program that plays Shannon's Game.

Work developed during COSC122-22SU2 by:

Tutor Author: Liam Laing
Email: liam.laing@canterbury.ac.nz

Student Author: Robert Ivill
Email: riv14@uclive.ac.nz
"""

import sys
import time
import re
from unicodedata import category

CORPUS_DIR = "data"
DEFAULT_CORPUS = f'{CORPUS_DIR}/corpus.txt'


class Frequency:
    """Stores a value : frequency pair"""

    def __init__(self, item, frequency):
        self.item = item
        self.frequency = frequency
        self.next_node = None

    def __repr__(self):
        return f'({repr(self.item)}, {repr(self.frequency)})'


class FrequencyList:
    """Stores a collection of Frequency objects as a linked list."""

    def __init__(self):
        """Creates an empty FrequencyList"""
        self.head = None

    def add(self, item, frequency=1):
        """
        If the given `item` is already in the list,
          the given frequency is added to its frequency.
        Otherwise adds the given item:frequency combination as a Frequency object
        to the end of the list.
        """
        # ---start student section---
        freq = self.__contains__(item)
        current = self.head
        if freq is False:
            new_node = Frequency(item, frequency)
            if current is None:
                self.head = new_node
                self.head.next_node = None
            else:
                while current.next_node is not None:
                    current = current.next_node
                current.next_node = new_node
        else:
            while current.item != item:
                current = current.next_node
            current.frequency += frequency        
        # ===end student section===

    def remove(self, item):
        """
        Removes the Frequency object with the given `value` from the list.
        Does nothing if `value` is not in the list.
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
        if current == None:
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
        while current != None:
            if current.item == item:
                return current
            current = current.next_node
        return None
        # ===end student section===

    def __contains__(self, item):
        """Returns True if item is in this FrequencyList
        Remember self.find(item) will return the index of the item
        if the item is in the list otherwise it returns None.
        """
        return self.find(item) is not None

    def __len__(self):
        """Returns the length of the FrequncyList, zero if empty
        """
        # ---start student section---
        current = self.head
        length = 0
        while current is not None:
            length += 1
            current = current.next_node
        return length
        # ===end student section===

    def __repr__(self):
        """ Returns a string representation of the list in the form:
        ('a', 2) -> ('b', 10) ... ->
        """
        current = self.head
        result = ''
        while current:
            result += repr(current) + ' -> '
            current = current.next_node
        return result.strip()


def possible_characters(corpus, last):
    """
    Returns a Python list of all instances of single characters in 'corpus' that
    immediately follow 'last' (including duplicates). The characters should be
    in that same order as they appear in the corpus

    The 'corpus' and 'last' should be all lowercase characters.
    Duplicates are included.

    >>> possible_characters('lazy languid line', 'la')
    ['z', 'n']
    """
    # ---start student section---
    result = []
    corpus1 = corpus.lower()
    last1 = last.lower()
    len_last = len(last1)
    for i in range(len(corpus1) - len_last):
            if corpus1[i:i+len_last] == last1:
                result.append(corpus[i+len_last])
    return result    
    # ===end student section===


def count_frequencies(items):
    """
    Counts the frequencies of each element in `items` and returns a
    FrequencyList of Frequency objects containing the element and frequency.
    The items in the returned LinkedList should be in the same order as they appear in the
    items list (they don't need to be sorted by frequency).

    >>> count_frequencies(['e', 'e', 'o'])
    ('e', 2) -> ('o', 1) ->
    """
    # ---start student section---
    FreqList = FrequencyList()
    for item in items:
        FreqList.add(item)
    return FreqList
    # ===end student section===


def select_next_guess(possibles):
    """
    Removes and returns the item with the highest frequency from the
    'possibles' FrequencyList.
    If more than one item has the highest frequency then the first
    item in the list with that frequency is returned.
    Returns None if there are no more guesses.
    """
    # ---start student section---
    highest_freq = 0
    current = possibles.head
    if current is not None:
        while current is not None:
            if highest_freq < current.frequency:
                highest_freq = current.frequency
                highest_item = current
            current = current.next_node
    else:
        return None
    possibles.remove(highest_item.item)
    return highest_item.item

    # ===end student section===


###############################################################################
#################### DO NOT MODIFY ANYTHING INSIDE THE BLOCK BELOW ############
################# There is some code below this block you should read #########
###############################################################################

def fallback_guesses(possibles):
    """
    Returns all characters from a--z, and some punctuation that don't appear in
    `possibles`.
    """
    all_fallbacks = [chr(c) for c in range(ord('a'), ord('z') + 1)] + \
                    [' ', ',', '.', "'", '"', ';', '?', '!']
    fallbacks = [x for x in all_fallbacks if x not in possibles]
    return fallbacks


def format_document(doc):
    """
    Re-formats `doc` by collapsing all whitespace characters into a space and
    stripping all characters that aren't letters or punctuation.
    """
    # http://www.unicode.org/reports/tr44/#General_Category_Values
    allowed_categories = ('Lu', 'Ll', 'Lo', 'Po', 'Zs')
    # d = unicode(d, 'utf-8')
    # d = str(d, 'utf-8')
    # Collapse whitespace
    doc = re.compile(r'\s+', re.UNICODE).sub(' ', doc)
    doc = u''.join([c.lower()
                   for c in doc if category(c) in allowed_categories])
    # Disable the encode to properly process a unicode corpus
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


def check_guesses(next_char, guesses):
    """
    Runs through `guesses` to check against `next_char` (or asks the user if
    `next_char` is None).
    If a correct guess is found, (guess, count) is returned; otherwise
    (None, count) is returned. Where `count` is the number of guesses
    attempted.
    """
    guess = select_next_guess(guesses)
    guess_count = 0
    while guess is not None:
        guess_count += 1
        if check_guess(next_char, guess):
            return guess, guess_count
        guess = select_next_guess(guesses)
    # Wasn't able to find a guess
    return None, guess_count


def check_fallback_guesses(next_char, guesses):
    """
    Runs through 'guesses' to check against 'next_char' (or asks the user if
    'next_char' is None).
    If a correct guess is found, (guess, count) is returned; otherwise
    (None, count) is returned. Where 'count' is the number of guesses
    attempted.
    """
    guess_count = 0
    for guess in guesses:
        guess_count += 1
        if check_guess(next_char, guess):
            return guess, guess_count

    print('Exhaused all fallbacks! Failed to guess phrase.')
    sys.exit(1)


def get_guesses_list(corpus, progress):
    """ Returns the frequency list of guesses
    Guesses should appear in the same order in the input file
    """
    pair = progress[-2:]
    possibles = possible_characters(corpus, pair)
    if possibles is None:
        sys.stderr.write('possible_characters has not been implemented!\n')
        sys.exit(1)

    guesses = count_frequencies(possibles)
    if guesses is None:
        sys.stderr.write('count_frequencies has not been implemented!\n')
        sys.exit(1)
    return guesses


def find_next_char(corpus, phrase, progress, is_auto):
    """ Keeps guessing until the right character is chosen.
    With crash and burn if can't guess it.
    """
    guesses = get_guesses_list(corpus, progress)
    fallbacks = fallback_guesses(guesses)
    # Figure out what the next character to guess is
    next_char = phrase[len(progress)].lower() if is_auto else None
    # Try to guess it from the corpus
    (guess, char_guess_count) = check_guesses(next_char, guesses)
    # If guessing from the corpus failed, try guessing from the fallbacks
    if guess is None:
        (guess, fb_count) = check_fallback_guesses(next_char, fallbacks)
        char_guess_count += fb_count
    return guess, char_guess_count


def play_game(corpus, phrase, phrase_len=0):
    """
    Plays the game.
      'corpus' is the complete corpus to use for finding guesses.
      'phrase' is the phrase to match, or part of the phrase.
      'phrase_len' is the total length of the phrase or 0 for auto mode
    If 'phrase_len' is zero, then the game is played automatically and
    the phrase is treated as the whole phrase. Otherwise the phrase is
    the start of the phrase and the function will ask the user whether
    or not it's guesses are correct - and keep going until phrase_len
    characters have been guessed correctly.

    Given phrase_len is 0 by default leaving out phrase_len from
    calls will auto-run, eg, play_game(corpus, 'eggs') will auto-run

    Returns the total number of guesses taken and the total time taken
    If in interactive mode the time taken value will be 0.
    """
    is_auto = phrase_len == 0
    if is_auto:
        phrase_len = len(phrase)
    progress = phrase[0:2]
    total_guesses = 0

    start = time.perf_counter()
    gap_line = '_' * (phrase_len - len(progress))
    print(f'{progress}{gap_line}  {total_guesses:02}')
    while len(progress) != phrase_len:
        next_char, guesses = find_next_char(corpus, phrase, progress, is_auto)
        total_guesses += guesses
        progress += next_char
        gap_line = '_' * (phrase_len - len(progress))
        print(f'{progress}{gap_line}  {guesses:02}')
    end = time.perf_counter()

    print(f'Solved in {total_guesses} guesses.')
    # return zero if in interactive mode
    time_taken = end - start if is_auto else 0
    return total_guesses, time_taken


def load_corpus_and_play(corpus_filename, phrase, length=0):
    """ Loads the corpus file and plays the game with the given setttings
    """
    with open(corpus_filename, encoding='utf-8') as infile:
        corpus = format_document(infile.read())
        _, time_taken = play_game(corpus, phrase, length)
        if length == 0:
            print(f'Took {time_taken:0.6f} seconds')


###############################################################################
#################### DO NOT MODIFY ANYTHING INSIDE THE BLOCK ABOVE ############
###############################################################################


################### Your Testing Code Goes in here ############################

def run_time_trials():
    """ A good place to write code for time trials.
    We have given you some example code to get you started.
    Make sure you use this docstring to explain your code and that
    you write comments in your code to help explain the process.
    """
    corpus_filename = f'{CORPUS_DIR}/war-and-peace.txt'  # try others if you want
    with open(corpus_filename, encoding='utf-8') as infile:
        print('Loading corpus ... ' + corpus_filename)
        full_corpus = format_document(infile.read())
    results = []
    phrase = 'fair dinkum'
    # we go up to 50000 in steps of 2000 for a start
    # you may want to go all the way to the length of the corpus
    # to see what happens.
    for size in range(1000, 50000, 2000):
        slice_of_corpus = full_corpus[0:size]  # then try [0:2000] etc
        num_guesses, time_taken = play_game(
            slice_of_corpus, phrase)  # play with autorun
        print(f'With corpus size {size:4} time taken = {time_taken}')
        results.append((size, num_guesses, time_taken))
    print('{:>6}  {:^12} {:^10}'.format('size', 'num_guesses', 'time_taken'))
    for size, num_guesses, time_taken in results:
        print(f'{size:6}  {num_guesses:^12}  {time_taken:^10.4f}')

    # As the corpus size increases the number of guesses generally falls
    # but why does the time increase?


def run_some_trials():
    """ Play some games with various test phrases and settings """
    # play game using whatever you like
    # maybe put an input statement here
    # so you can enter the corpus
    # and settings
    # or just run various games with various settings

    # MAKE SURE you test with various phrases!
    test_phrases = ["is it weird to have  two spaces in here?",
                    'dead war',
                    'Extreme emotional experiment', 
                    'the quick brown fox jumped over the lazy dog',
                    ]
    test_files = [DEFAULT_CORPUS,
                  # Some other file names
                  #f'{CORPUS_DIR}/the-yellow-wall-paper.txt',
                  #f'{CORPUS_DIR}/hamlet.txt',
                  #f'{CORPUS_DIR}/le-rire.txt',
                  #f'{CORPUS_DIR}/war-of-the-worlds.txt',
                  #f'{CORPUS_DIR}/ulysses.txt',
                  #f'{CORPUS_DIR}/war-and-peace.txt'
                  ]

    # Uncomment the block below to run trials based on the lists of phrases
    # and files above
    for test_phrase in test_phrases:
        for corpus_filename in test_files:
            phrase_length = 0  # for auto-run
            load_corpus_and_play(corpus_filename, test_phrase, phrase_length)
            print('\n' * 3)

    # check out https://www.gutenberg.org/ for more free books!


def test():
    """ Runs doctests and other trials"""

    # Running trials
    # -----------------
    # Uncomment the call to run_some_trials below to run
    # whatever trials you have setup in that function
    # IMPORTANT: comment out the run_some_trials() line below
    # before you submit your code
    run_some_trials()

    # Time trials
    # -----------------
    # Running time trials will give you a feel for how the speed
    # is affected by the corpus size
    run_time_trials()

    # interactive trial
    # -----------------
    # see how long the program takes to guess 'bat man'
    # it will get the first two characters and start asking you
    # if it has the third character correct etc...
    # load_corpus_and_play(f'{CORPUS_DIR}/le-rire.txt', 'ba', 7)


################# End of Testing Code ########################################


def main():
    """ Put your calls to testing code here.
    The quiz server will not run this function.
    It will test directly
    """
    test()


# run this code if not being imported
if __name__ == '__main__':
    main()
    # don't add any code here
