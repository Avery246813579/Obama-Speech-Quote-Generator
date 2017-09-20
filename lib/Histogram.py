import random


class Histogram:
    """ Histogram is a class to store types and tokens

     We store all our data in an array of arrays. The internal arrays we will be calling nodes. Each node represents
     a respected number of word occurrences. The node has three values at the indexes 0, 1, 2.

     0: The number of occurrences
     1: The words that occur (0) amount of times
     2: The chance we will pick this number based on the last numbers
     """

    def __init__(self):
        """ Initialize the data """
        self.nodes = []
        self.word_count = 0

    def __len__(self):
        """ Gets the amount of words in the data set. Not types! """
        return self.word_count

    def __str__(self):
        """ THe string representation of the nodes """
        return str(self.nodes)

    def calculate_percents(self):
        """ Calculate the chance that a list of numbers will come up in relation to the whole set of words. """
        last_percent = 0
        word_count = self.word_count

        for i in range(len(self.nodes)):
            current_node = self.nodes[i]

            # If we already have calculated the data before just update the number. If not, append the percent to the
            # current node.
            if len(self.nodes[i]) > 2:
                current_node[2] = last_percent + current_node[0] * len(current_node[1]) / word_count
            else:
                current_node.append(last_percent + current_node[0] * len(current_node[1]) / word_count)

                last_percent += current_node[0] / word_count * len(current_node[1])

    # UNiuque me

    def update_word(self, word):
        """ If the word is already in the histogram we will update the number of times the word occurs. If not then
        we insert it into our nodes

        :param word:     The word we want update in the data set
        """

        self.word_count += 1
        length = len(self.nodes)

        if length < 1:
            self.nodes.append([1, [word]])
            return

        ## Zip staggered
        for i in range(length):
            if word in self.nodes[i][1]:
                self.nodes[i][1].remove(word)

                if i > length - 2:
                    self.nodes.append([self.nodes[i][0] + 1, [word]])
                else:
                    if self.nodes[i + 1][0] == self.nodes[i][0] + 1:
                        self.nodes[i + 1][1].append(word)
                    else:
                        self.nodes.insert(i + 1, [self.nodes[i][0] + 1, [word]])

                if len(self.nodes[i][1]) < 1:
                    del self.nodes[i]

                return

        if self.nodes[0][0] == 1:
            self.nodes[0][1].append(word)
        else:
            self.nodes.insert(0, [1, [word]])

    def random_word(self):
        number = random.random()

        for i in range(len(self.nodes)):
            if number < self.nodes[i][2]:
                return self.nodes[i][1][random.randint(0, len(self.nodes[i][1]) - 1)]

    def frequency(self, key):
        if key in self.nodes:
            return self.nodes[key]
