import random

from lib.Histogram import Histogram
from lib.FileParser import FileParser
import collections


class Dictogram:
    """ A Dictogram is a custom data type we use to store data for our Markov Chain. We use key (a word or phrase) then
    a histogram (of following words or phrases) to store our data.

    I refer to key and value a lot during this class. A key is the current word or phrase we are looking at (it can be
    a word of phrase because of the order we are using). A value is the word or phrase following our current key.
     """

    def __init__(self, file, order):
        """ Constructing the Dictogram

        :param file:        The file location we want to read from (the corpus)
        :param order:       The Markov Chain order
        """

        parser = FileParser(file)
        words = parser.words
        words_length = len(words)

        # Used to find the start of sentences
        self.sentence_ends = []

        self.word_count = words_length
        self.line_count = len(parser.lines)
        self.data = dict()

        # We loop through all our words and if it has occurred we add the following word to a histogram. If it has not
        # occurred we construct a new histogram
        for i in range(words_length):
            # We need to add [NONE] characters to the end of the word list because there are no words (or phrases in
            # order > 1 case) left to follow
            if i > words_length - (order + 1):
                self.add(words[i], '[NONE]')
                continue

            pre_window = ' '.join(words[i: i + order])
            window = ' '.join(words[i + 1: i + order + 1])

            # If the word is the sentence end token, we add this key to a end key list
            if words[i] == "[NONE]":
                self.sentence_ends.append(pre_window)

            # Add current data to our Dictogram
            self.add(pre_window, window)

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
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    test = collections.deque(numbers[0: 3])

    for _ in range(3, len(numbers)):
        test.popleft()
        test.append()

    print("HI", test)

