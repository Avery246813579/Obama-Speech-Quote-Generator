import random

from Histogram import Histogram
from collections import deque


class Dictogram:
    """ A Dictogram is a custom data type we use to store data for our Markov Chain. We use key (a word or phrase) then
    a histogram (of following words or phrases) to store our data.

    I refer to key and value a lot during this class. A key is the current word or phrase we are looking at (it can be
    a word of phrase because of the order we are using). A value is the word or phrase following our current key.
     """

    def __init__(self, words, order, backwords = False):
        """ Constructing the Dictogram

        :param words:       The words you want to add (the corpus)
        :param order:       The Markov Chain order
        """

        words_length = len(words)
        window = deque(words[0: order])

        # Used to find the start of sentences
        self.sentence_ends = [tuple(window)]

        self.word_count = words_length
        self.data = dict()

        # We loop through all our words and if it has occurred we add the following word to a histogram. If it has not
        # occurred we construct a new histogram
        for i in range(order, words_length - 1):
            current_word = words[i]
            
            self.next_item(window, current_word)

    def next_item(self, window, word):
        split = False
        if word[-1] == '.':
            word = word[:-1]
            split = True

        # Add current data to our Dictogram
        self.add(tuple(window), word)

        # Add the next number in the sequence
        window.append(word)

        # Remove the left number in the sequence
        if window.popleft() == '[SPLIT]':
            self.sentence_ends.append(tuple(window))

        # End of Word
        if split:
            self.next_item(window, '[SPLIT]')

    def random_start(self):
        """ Finds a random start to our sentence using the end keys list.

        :return:        A key to use in order to construct the start of a sentence
        """
        return self.sentence_ends[random.randint(0, len(self.sentence_ends) - 1)]

    def add(self, key, value):
        """ Adds a key-value pair to the data set.

         :param key:        The word or phrase that we are currently looking at
         :param value:      The value is the word or phrase following the key
         """

        # If the word or phrase has not been said before, we create a new histogram for that word.
        if key not in self.data:
            self.data[key] = Histogram()

        # Update the word phrase in the keys histogram
        self.data[key].update_word(value)

    def random_key(self):
        """ Gets a random word or phrase from our data set """
        keys = list(self.data.keys())

        return keys[random.randint(0, len(keys) - 1)]

    def __str__(self):
        return str(self.data)


if __name__ == "__main__":
    test_dict = Dictogram(list(reversed(['Hi', 'Mom', 'How', 'Are', 'You.', 'I', 'am', 'doing', 'Good.'])), 1, True)
    print(str(test_dict))