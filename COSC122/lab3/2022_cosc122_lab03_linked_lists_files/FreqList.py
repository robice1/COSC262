"""FrequencyList classes and testing routines.
Work through the lab handout to find out what you are doing..."""

import time
import re
import os
import doctest
from unicodedata import category
import matplotlib.pyplot as plt

os.environ['TERM'] = 'linux'  # Suppress ^[[?1034h


#-------------------------------------------------------------------------
class FreqNode(object):
    """Stores an item, frequency pair.

    Basically a FreqNode object is a node in the frequency list.
    Each FreqNode holds an item, the frequency for the item,
    and a pointer to the next FreqNode object (or None).

    >>> f = FreqNode('c', 2)
    >>> f.item
    'c'
    >>> f.frequency
    2
    >>> print(f)
    'c' = 2
    """

    def __init__(self, item, frequency=1):
        self.item = item
        self.frequency = frequency
        self.next_node = None

    def increment(self):
        """ Add one to the frequency count for this item """
        self.frequency += 1

    def __str__(self):
        return f"'{self.item}' = {self.frequency}"


#-------------------------------------------------------------------------
class FreqList(object):
    """Stores a linked list of FreqNode objects.
    NOTE: This is a parent class for Unsorted, NicerUnSorted & Sorted FreqLists
    """

    def __init__(self):
        self.head = None
        self.freq_list_type = 'Generic parent'

    def add(self, item):
        """Will be implemented by child classes. Don't write anything here.
        This will add an item with frequency=1 if item not in list,
        otherwise it will increment the frequency count for the item.
        """
        current = self.head 
        in_list = False
        while current != None:
            if current.item == item:
                in_list = True  # data found
            current = current.next_node
        if in_list == True:
            current.frequency += 1
        else:
            new_node = Node(item)
            new_node.next_node = self.head
            self.head = new_node            
  

    def get_item_frequency(self, item):
        """Returns Frequency of item, if found else returns 0.

        **** NOTE: Don't use this when writing your add methods. ****

        That is, you should scan through the list directly when adding.
        Using this method to check for existence of an item will be
        very inefficient... think about why.
        """
        current = self.head
        while current is not None:
            if current.item == item:
                return current.frequency
            current = current.next_node
        return 0

    def get_xy_for_plot(self):
        """ Returns two lists that can be used for plotting
        items and frequencies.
        The first contains the items and the second contains the frequecies.
        """
        x_values = []
        y_values = []
        curr_item = self.head
        while curr_item is not None:
            # use repr of items so that spaces show, eg, 'e '
            x_values.append(repr(curr_item.item))
            y_values.append(curr_item.frequency)
            curr_item = curr_item.next_node
        return x_values, y_values

    def _max_index_width(self):
        """
        Returns widest index width + 2
        For example, if there are 100 items in the list
        then 100 is the maximum item number and it is 3 characters wide,
        so set the width for the index column to 5
        """
        length = len(self)
        return len(str(length)) + 2

    def __len__(self):
        """Returns the number of nodes in the freq. list. Zero if empty."""
        current = self.head
        length = 0
        while current is not None:
            length += 1
            current = current.next_node
        return length

    def __str__(self):
        """Returns the items together with their letter frequencies."""
        result = self.freq_list_type + '\n'
        result += '-' * 35 + '\n'
        line_strs = []
        current_node = self.head
        max_index_width = self._max_index_width()
        node_num = 1
        while current_node is not None:
            line_str = f'{node_num:>{max_index_width}}:  {str(current_node)}'
            line_strs.append(line_str)
            current_node = current_node.next_node
            node_num += 1
        return result + '\n'.join(line_strs)
    
    
    