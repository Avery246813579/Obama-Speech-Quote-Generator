import random

from Histogram import Histogram
from FileParser import FileParser


class Dictogram:
    """

    """

    def __init__(self, file, order):
        parser = FileParser(file)

        words = parser.words
        length = len(words)

        self.word_count = length
        self.line_count = len(parser.lines)

        self.data = dict()

        for i in range(length):
            if i > length - 4:
                self.add(words[i], '[NONE]')
                continue

            self.add(' '.join(words[i: i + order]), ' '.join(words[i + 1: i + order + 1]))

    def add(self, dta, value):
        if dta not in self.data:
            self.data[dta] = Histogram()

        self.data[dta].update_word(value)

    def random_key(self):
        keys = list(self.data.keys())

        return keys[random.randint(0, len(keys) - 1)]

    def __str__(self):
        return str(self.data)
