import random

from Main import FileParser, Histogram


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

        for key in self.data:
            self.data[key].calculate_percents()

    def add(self, dta, value):
        if dta not in self.data:
            self.data[dta] = Histogram()

        self.data[dta].add(value)

    def random_key(self):
        keys = list(self.data.keys())

        return keys[random.randint(0, len(keys) - 1)]

    def __str__(self):
        return str(self.data)


class MarkovModel:
    def __init__(self, corpus, order):
        self.map_gram = Dictogram(corpus, order)

    def generate_sentence(self, length):
        to_return = ''

        element = None
        for i in range(length):
            word = None

            if element is None:
                word = self.map_gram.random_key()
                element = self.map_gram.data[word]
                word = " " + word.split(" ")[0]
            else:
                word = element.random_word()

                if word == "[NONE]":
                    word = self.map_gram.random_key()
                    element = self.map_gram.data[word]
                    word = ". " + word.split(" ")[0]
                else:
                    element = self.map_gram.data[word]
                    word = " " + word.split(" ")[0]

            to_return += word

        return to_return[1:].capitalize()

    def __str__(self):
        return str()


if __name__ == '__main__':
    model = MarkovModel("static/test_data.txt", 3)

    print("Booted")
    print(model.generate_sentence(20))
    print("Booted")
    print(model.generate_sentence(20))

