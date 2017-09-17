import random

def randomSentence(letters):
    file = open("/usr/share/dict/words", "r")

    array = file.read().splitlines()
    length = len(array)
    to_return = ''

    for i in range(letters):
        to_return += array[random.randint(0, length) - 1] + " "

    return to_return


class Generator:
    def __init__(self, file):
        self.file = FileParser(file)
        self.histogram = Histogram(self.file.words)

    def generate_sentence(self, length):
        to_return = ''

        for i in range(length):
            to_return += self.histogram.random_word() + " "

        return to_return


# Parser to parse the words and lines from a text file
class FileParser:
    def __init__(self, file):
        file = open(file, "r")
        self.lines = file.read().splitlines()

        self.words = []
        for i in range(len(self.lines)):
            self.words += self.lines[i].split()


# Histogram class used to store our words
class Histogram:
    def __init__(self):
        self.data = []
        self.raw = 0

        self.calculate_percents()

    # Calculates the percentages a certain set of words occur and stres it at the third index in their respected array
    def calculate_percents(self):
        last = 0

        for i in range(len(self.data)):
            if len(self.data[i]) > 2:
                self.data[i][2] = last + self.data[i][0] * len(self.data[i][1]) / self.raw
            else:
                self.data[i].append(last + self.data[i][0] * len(self.data[i][1]) / self.raw)

            last += self.data[i][0] / self.raw * len(self.data[i][1])

    # Adds an element to the histogram
    def add(self, key):
        self.raw += 1
        length = len(self.data)

        if length < 1:
            self.data.append([1, [key]])
            return

        for i in range(length):
            if key in self.data[i][1]:
                self.data[i][1].remove(key)

                if i > length - 2:
                    self.data.append([self.data[i][0] + 1, [key]])
                else:
                    if self.data[i + 1][0] == self.data[i][0] + 1:
                        self.data[i + 1][1].append(key)
                    else:
                        self.data.insert(i + 1, [self.data[i][0] + 1, [key]])

                if len(self.data[i][1]) < 1:
                    del self.data[i]

                return

        if self.data[0][0] == 1:
            self.data[0][1].append(key)
        else:
            self.data.insert(0, [1, [key]])

    # Get's the number of words in the histogram
    def __len__(self):
        return self.raw

    # Get's a random word from the histogram
    def random_word(self):
        number = random.random()

        for i in range(len(self.data)):
            if number < self.data[i][2]:
                return self.data[i][1][random.randint(0, len(self.data[i][1]) - 1)]

    # Gets the frequency of the word
    def frequency(self, key):
        if key in self.data:
            return self.data[key]

    def __str__(self):
        return str(self.data)


if __name__ == '__main__':
    array = ["dog"]
    dog = array.copy()

    print(dog)
    print(array)
