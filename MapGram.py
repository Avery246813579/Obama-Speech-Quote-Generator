import Main
import random


class MapGram:
    # Convert this dictionary to a Histogram

    def __init__(self, file):
        words = Main.FileParser(file).words
        length = len(words)
        print(length)

        self.data = dict()

        for i in range(length):
            if i > length - 4:
                self.add(words[i], '-<NONE>-')
                continue

            self.add(words[i] + " " + words[i + 1] + " " + words[i + 2], words[i + 1] + " " + words[i + 2] + " " + words[i + 3])

        for key in self.data:
            self.data[key].calculate_percents()

    def add(self, dta, value):
        if dta not in self.data:
            self.data[dta] = Main.Histogram()

        self.data[dta].add(value)

    def random_key(self):
        keys = list(self.data.keys())

        return keys[random.randint(0, len(keys) - 1)]

    def __str__(self):
        return str(self.data)


class MarkovModel:
    def __init__(self, corpus):
        self.map_gram = MapGram(corpus)

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

                if word == "-<NONE>-":
                    word = self.map_gram.random_key()
                    element = self.map_gram.data[word]
                    word = ". " + word.split(" ")[0]
                else:
                    element = self.map_gram.data[word]
                    word = " " + word.split(" ")[0]

            to_return += word

        return to_return[1:]

    def __str__(self):
        return str()


if __name__ == '__main__':
    model = MarkovModel("test_data.txt")

    print("Booted")
    print(model.generate_sentence(20))
    print("Booted")
    print(model.generate_sentence(20))
    print(model.generate_sentence(20))
    print(model.generate_sentence(20))
    print(model.generate_sentence(20))

