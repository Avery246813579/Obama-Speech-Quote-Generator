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
    data = {}
    raw = 0

    def __init__(self, words):
        for i in range(len(words)):
            self.add(words[i], None)

    def add(self, key, value):
        self.raw += 1

        if key in self.data:
            self.data[key] += 1
        else:
            self.data[key] = 1

    def length(self):
        return len(self.data)

    def frequency(self, key):
        if key in self.data:
            return self.data[key]

    def __str__(self):
        return str(self.data)

file = FileParser("test_data.txt")
gram = Histogram(file.words)
print(gram.frequency("fish"))
