import random

"""
1. Code cleanup
2. Start End
3. Speed and Efficiency
4. Hidden 
"""


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

    def __len__(self):
        return self.raw

    def calculate_percents(self):
        """ Calculates
        """
        last = 0

        for i in range(len(self.data)):
            if len(self.data[i]) > 2:
                self.data[i][2] = last + self.data[i][0] * len(self.data[i][1]) / self.raw
            else:
                self.data[i].append(last + self.data[i][0] * len(self.data[i][1]) / self.raw)

            last += self.data[i][0] / self.raw * len(self.data[i][1])

    # UNiuque me

    def add(self, key):
        self.raw += 1
        length = len(self.data)

        if length < 1:
            self.data.append([1, [key]])
            return

        ## Zip staggered
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


if __name__ == '__main__':
    array = ["dog"]
    dog = array.copy()

    print(dog)
    print(array)
