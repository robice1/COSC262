def change_greedy(amount, coinage):
    """takes an integer amount of money in some units plus a list of integer 
    coin values and returns the breakdown of that amount of coins (greedy)"""
    coinage.sort(reverse=True)
    coins_used = []
    for coin in coinage:
        while amount > 0:
            if coin <= amount:
                coins_used.append(coin)
                amount -= coin
            else:
                break
    breakdown = []
    if amount == 0:
        for coin in sorted(set(coins_used), reverse=True):
            n = coins_used.count(coin)
            breakdown.append((n, coin))
        return breakdown
    else:
        return None

def print_shows(show_list):
    show_list.sort(key=lambda x: x[1] + x[2])
    s = []
    t_current = 0
    for i in range(len(show_list)):
        if show_list[i][1] >= t_current:
            s.append(show_list[i])
            t_current = show_list[i][2] + show_list[i][1]
    for show in s:
        print(f"{show[0]} {show[1]} {show[2] + show[1]}")

def fractional_knapsack(capacity, items):
    items.sort(key=lambda x: x[1] / x[2], reverse = True)
    benefit = 0
    for item in items:
        if capacity == 0:
            break
        if item[2] <= capacity:
            benefit += item[1]                
            capacity -= item[2]
        else:
            benefit += item[1] * capacity / item[2]
            capacity = 0
    return benefit

"""An incomplete Huffman Coding module, for use in COSC262.
   Richard Lobb, April 2021.
"""
import heapq
import re

HAS_GRAPHVIZ = True
try:
    from graphviz import Graph
except ModuleNotFoundError:
    HAS_GRAPHVIZ = False

class Node:
    """Represents an internal node in a Huffman tree. It has a frequency count,
       minimum character in the tree, and left and right subtrees, assumed to be
       the '0' and '1' children respectively. The frequency count of the node
       is the sum of the children counts and its minimum character (min_char)
       is the minimum of the children min_chars.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.count = left.count + right.count
        self.min_char = min(left.min_char, right.min_char)

    def __repr__(self, level=0):
        return ((2 * level) * ' ' + f"Node({self.count},\n" +
            self.left.__repr__(level + 1) + ',\n' +
            self.right.__repr__(level + 1) + ')')

    def is_leaf(self):
        return False

    def plot(self, graph):
        """Plot the tree rooted at self on the given graphviz graph object.
           For graphviz node ids, we use the object ids, converted to strings.
        """
        graph.node(str(id(self)), str(self.count)) # Draw this node
        if self.left is not None:
            # Draw the left subtree
            self.left.plot(graph)
            graph.edge(str(id(self)), str(id(self.left)), '0')
        if self.right is not None:
            # Draw the right subtree
            self.right.plot(graph)
            graph.edge(str(id(self)), str(id(self.right)), '1')


class Leaf:
    """A leaf node in a Huffman encoding tree. Contains a character and its
       frequency count.
    """
    def __init__(self, count, char):
        self.count = count
        self.char = char
        self.min_char = char

    def __repr__(self, level=0):
        return (level * 2) * ' ' + f"Leaf({self.count}, '{self.char}')"

    def is_leaf(self):
        return True

    def plot(self, graph):
        """Plot this leaf on the given graphviz graph object."""
        label = f"{self.count},{self.char}"
        graph.node(str(id(self)), label) # Add this leaf to the graph
        


class HuffmanTree:
    """Operations on an entire Huffman coding tree.
    """
    def __init__(self, root=None):
        """Initialise the tree, given its root. If root is None,
           the tree should then be built using one of the build methods.
        """
        self.root = root
        
    def encode(self, text):
        """Return the binary string of '0' and '1' characters that encodes the
           given string text using this tree.
        """
        leaf_paths = {}
        self.traverse(self.root, leaf_paths, '')
        result = ''
        for char in text:
            result += leaf_paths[char]
        return result
        
        
    def traverse(self, node, leaf_paths, path_so_far):
        if isinstance(node, Leaf):
            leaf_paths[node.char] = path_so_far
        else:
            self.traverse(node.left, leaf_paths, path_so_far + '0')
            self.traverse(node.right, leaf_paths, path_so_far + '1')
        
    def decode(self, binary):
        """Return the text string that corresponds the given binary string of
           0s and 1s
        """
        if self.root is None:
            return
        else:
            decoding = ""
            node = self.root
            for num in binary:
                if num == "0":
                    node = node.left
                else:
                    node = node.right
                if node.is_leaf():
                    decoding += node.char
                    node = self.root
        return decoding

    def plot(self):
        """Plot the tree using graphviz, rendering to a PNG image and
           displaying it using the default viewer.
        """
        if HAS_GRAPHVIZ:
            g = Graph()
            self.root.plot(g)
            g.render('tree', format='png', view=True)
        else:
            print("graphviz is not installed. Call to plot() aborted.")

    def __repr__(self):
        """A string representation of self, delegated to the root's repr method"""
        return repr(self.root)


    def build_from_freqs(self, frequencies):
        """Builds the Huffman coding tree from the given character frequencies."""
        # Build the list of trees and sort by frequency
        table = [(k, v) for k, v in frequencies.items()]
        table.sort(key = lambda x: x[1])
        while len(table) > 1:
            left = table.pop()
            right = table.pop()
            left_leaf = Leaf(left[1], left[0])
            right_leaf = Leaf(right[1], right[0])
            new_node = Node(left_leaf, right_leaf)
            table.append((new_node, new_node.count))
            table.sort(key = lambda x: x[1])
        self.root = table.pop()[0]

    def build_from_string(self, s):
        """Convert the string representation of a Huffman tree, as generated
           by its __str__ method, back into a tree (self). There are no syntax
           checks on s so it had better be valid!
        """
        s = s.replace('\n', '')  # Delete newlines
        s = re.sub(r'Node\(\d+,', 'Node(', s)
        self.root = eval(s)


def main():
    """ Demonstrate defining a Huffman tree from its string representation and
        printing and plotting it (if plotting is enabled on your machine).
    """
    tree = HuffmanTree()
    tree_string = """Node(42,
      Node(17,
        Leaf(8, 'b'),
        Leaf(9, 'a')),
      Node(25,
        Node(10,
          Node(5,
            Leaf(2, 'f'),
            Leaf(3, 'd')),
          Leaf(5, 'e')),
        Leaf(15, 'c')))
    """
    tree.build_from_string(tree_string)
    print(tree)
    tree.plot()
    
    # Or you can build the tree directly
    tree2 = HuffmanTree(Node(
      Node(
        Leaf(8, 'b'),
        Leaf(9, 'a')),
      Node(
        Node(
          Node(
            Leaf(2, 'f'),
            Leaf(3, 'd')),
          Leaf(5, 'e')),
        Leaf(15, 'c'))))
    print(tree2)
    tree2.plot()
    
freqs = {'a': 9,
         'b': 8,
         'c': 15,
         'd': 3,
         'e': 5,
         'f': 2}
tree = HuffmanTree()
tree.build_from_freqs(freqs)
print(tree)