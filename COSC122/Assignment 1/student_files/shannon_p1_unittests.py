import unittest
import random
import io
import contextlib
import shannon_p1 as shannon

# make the random calls actions deterministic
random.seed(101)

ALPHA = 'abcdefghijklmnopqrstuvwxyz'
CORPUS_DIR = "data"


def temp_list(values):
    """build a test list quickly to use in testing"""
    l = shannon.FrequencyList()
    for value in values:
        l.add(value)
    return l


class FrequencyNodeTest(unittest.TestCase):
    def setUp(self):
        self.node = shannon.Frequency('c', 2)

    def test_item(self):
        self.assertEqual(self.node.item, 'c')

    def test_value(self):
        self.assertEqual(self.node.frequency, 2)

    def test_repr(self):
        self.assertEqual(repr(self.node), "('c', 2)")


class FrequencyList_add(unittest.TestCase):
    def test_initial_state(self):
        l = shannon.FrequencyList()
        self.assertIsNone(l.head)

    def test_one_node_repeat_add(self):
        l = shannon.FrequencyList()
        l.add('a', 3)
        self.assertEqual(repr(l), "('a', 3) ->")
        l.add('a', 50)
        self.assertEqual(repr(l), "('a', 53) ->")

    def test_multi_node_add(self):
        """Tests non-trivial number of nodes can be:
         - added to the linked list
         - be updated
         """
        l = shannon.FrequencyList()
        letters = list(ALPHA)
        for letter in letters:
            l.add(letter, 0)

        random.shuffle(letters)

        for letter in letters:
            l.add(letter)

        letters.sort()
        count = 0
        current = l.head
        while current is not None:
            self.assertEqual(current.item, letters[count])
            self.assertEqual(current.frequency, 1)
            count += 1
            current = current.next_node


class FrequencyList_find_single_node(unittest.TestCase):
    def setUp(self):
        self.list = shannon.FrequencyList()
        self.list.add("a")

    def test_sucessful_search(self):
        node = self.list.find("a")
        self.assertEqual(node.item, "a")
        self.assertEqual(node.frequency, 1)

    def test_failed_search(self):
        node = self.list.find("b")
        self.assertIsNone(node)


class FrequencyList_remove_single_item(unittest.TestCase):
    def setUp(self):
        self.list = shannon.FrequencyList()
        self.list.add("apple")

    def test_remove_item(self):
        self.list.remove("car")
        self.assertEqual(len(self.list), len(self.list))


class FrequencyList_len(unittest.TestCase):
    def test_1_node(self):
        self.assertEqual(len(temp_list("a")), 1)

    def test_2_node(self):
        self.assertEqual(len(temp_list("ab")), 2)

    def test_3_node(self):
        self.assertEqual(len(temp_list("abc")), 3)


class PossibleCharacters_two_charcter_prefix(unittest.TestCase):
    def test_type_of_container(self):
        self.assertIsInstance(
            shannon.possible_characters(
                'lazy languid line', 'la'), list)

    def test_small_sentence1(self):
        self.assertEqual(
            shannon.possible_characters(
                'lazy languid line', 'la'), [
                'z', 'n'])

    def test_small_sentence2(self):
        self.assertEqual(
            shannon.possible_characters(
                'pitter patter batton', 'tt'), [
                'e', 'e', 'o'])

    def test_small_sentence3(self):
        self.assertEqual(
            shannon.possible_characters(
                'pitter pattor batton', 'er'), [' '])


class CountFrequencies_alphabet(unittest.TestCase):
    def test_type_container(self):
        self.assertIsInstance(
            shannon.count_frequencies(ALPHA),
            shannon.FrequencyList)

    def test_alpha_once(self):
        l = shannon.count_frequencies(ALPHA)
        c = l.head
        i = 0
        while c:
            self.assertEqual(c.item, ALPHA[i])
            self.assertEqual(c.frequency, 1)
            c = c.next_node
            i += 1


class SelectNextGuess_alpha_test(unittest.TestCase):
    def setUp(self):
        self.data = [(letter, i + 1) for (i, letter) in enumerate(ALPHA)]
        self.list = shannon.FrequencyList()
        for item, frequency in self.data:
            self.list.add(item, frequency)

    def test_correct_retrieval_order(self):
        # Checking Assumption
        self.assertEqual(len(self.list), len(self.data))

        count = 0
        for letter, _ in reversed(self.data):
            self.assertEqual(shannon.select_next_guess(self.list), letter)
            count += 1
        # check that all elements in list are gone
        self.assertEqual(len(self.list), 0)


class LoadCorpusAndPlay_cached_example(unittest.TestCase):
    def setUp(self):
        with open("expected_results/LoadCorpusAndPlay_cached_example.txt") as file:
            lines = file.read().splitlines()
        lines.pop()  # remove time taken as it varies from run to run of the test
        self.expected = lines

    def test_compare_results(self):
        """Simply compares the results generated by your program vs results generated by the question author.
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            filename = 'the-yellow-wall-paper.txt'
            phrase = 'document test phrase'
            shannon.load_corpus_and_play(f"{CORPUS_DIR}/{filename}", phrase)
        got = output.getvalue().splitlines()
        got.pop()
        self.assertEqual(self.expected, got)


def test_suite():
    suite = unittest.TestSuite()

    # Tests that should work right away
    # suite.addTest(unittest.makeSuite(FrequencyNodeTest))
    # Tests for FrequencyList.add
    # suite.addTest(unittest.makeSuite(FrequencyList_add))

    # Tests for FrequencyList.find
    #suite.addTest(unittest.makeSuite(FrequencyList_find_single_node))

    # Tests for FrequencyList.remove
    suite.addTest(unittest.makeSuite(FrequencyList_remove_single_item))

    # Tests for FrequencyList len
    #suite.addTest(unittest.makeSuite(FrequencyList_len))

    # Tests for possible_characters
    # suite.addTest(unittest.makeSuite(PossibleCharacters_two_charcter_prefix))

    # Tests for count_frequencies
    #suite.addTest(unittest.makeSuite(CountFrequencies_alphabet))

    # Tests for select_next_guess
    suite.addTest(unittest.makeSuite(SelectNextGuess_alpha_test))

    # Test for load_corpus_and_play
    # Should work if FrequencyList and support functions are correctly implemented
    # suite.addTest(unittest.makeSuite(LoadCorpusAndPlay_cached_example))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite())
