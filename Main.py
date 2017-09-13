import random
import time

# args = ["Test", "Dog", "cat"]
#
# to_print = ''
# while len(args) > 0:
#     item = args[random.randint(0, len(args) - 1)]
#     to_print += item + " "
#     args.remove(item)
#
# print(to_print)

def randomSentence(letters):
    file = open("/usr/share/dict/words", "r")

    array = file.read().splitlines()
    length = len(array)
    to_return = ''

    for i in range(letters):
        to_return += array[random.randint(0, length) - 1] + " "

    return to_return


class FileParser:
    def __init__(self, file):
        file = open(file, "r")
        self.lines = file.read().splitlines()

        self.words = []
        for i in range(len(self.lines)):
            self.words += self.lines[i].split()


class Histogram:
    data = []
    raw = 0

    def __init__(self, words):
        for i in range(len(words)):
            self.add(words[i])

        self.calculate_percents()

    def calculate_percents(self):
        last = 0

        for i in range(len(self.data)):
            if len(self.data[i]) > 2:
                self.data[i][2] = last + self.data[i][0] * len(self.data[i][1]) / self.raw
            else:
                self.data[i].append(last + self.data[i][0] * len(self.data[i][1]) / self.raw)

            last += self.data[i][0] / self.raw * len(self.data[i][1])

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
            self.data.insert(0, [key])

    def length(self):
        return len(self.data)

    def random_word(self):
        number = random.random()

        for i in range(len(self.data)):
            if number < self.data[i][2]:
                return self.data[i][1][random.randint(0, len(self.data[i][1]) - 1)]

    def frequency(self, key):
        if key in self.data:
            return self.data[key]

    def __str__(self):
        return str(self.data)

file = FileParser("test_data.txt")
gram = Histogram(file.words)

