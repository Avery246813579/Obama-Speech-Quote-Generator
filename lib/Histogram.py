import random


class Histogram:
    """ Histogram is a class to store types and tokens

     We store all our data in an array of arrays. The internal arrays we will be calling nodes. Each node represents
     a respected number of word occurrences. The node has three values at the indexes 0, 1, 2.

     0: The number of occurrences
     1: The words that occur (0) amount of times
     2: The chance we will pick this number based on the last numbers
     """

    # TODO: Try flipping the nodes so that the greater number of occurrencs are lower indexes
    # TODO: Try to stagger the update using a staggered zip

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
        """ Calculate the chance that a list of numbers will come up in relation to the whole set of words. We use
         a range to make it easier later down the line and make generating words much faster and more efficient.

         """
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

        # If we have no data. Let's just create a new node.
        if length < 1:
            self.nodes.append([1, [word]])
            return

        for i in range(length):
            current_node = self.nodes[i]
            words = current_node[1]

            # If our word is in the current node. Remove it then check more things.
            if word in words:
                words.remove(word)

                # If there are no following nodes. We are the greatest node and can just add a new node
                if i > length - 2:
                    self.nodes.append([current_node[0] + 1, [word]])
                else:
                    next_node = self.nodes[i + 1]

                    # If the next nodes occurrences is equal to one more then the current node. We add our word to the
                    # next node. If not, then we create a new node there.
                    if next_node[0] == current_node[0] + 1:
                        next_node[1].append(word)
                    else:
                        self.nodes.insert(i + 1, [current_node[0] + 1, [word]])

                # If there are no words left in this node. We delete the node.
                if len(words) < 1:
                    del self.nodes[i]

                return

        # We check if the first nodes occurrences is 1. If it is we add our word. If not, we create a new node that
        # the occurrences is one
        if self.nodes[0][0] == 1:
            self.nodes[0][1].append(word)
        else:
            self.nodes.insert(0, [1, [word]])

    def random_word(self):
        """ Gets a random word from the histogram

        :return:    The random word
        """

        number = random.random()
        for i in range(len(self.nodes)):

            node = self.nodes[i]
            frequency = node[2]

            # If the number is greater then the percentage we calculated before, then this is the random node we want.
            # Then we get a random word from the node's second index which is the list of words
            if number < frequency:
                return node[1][random.randint(0, len(node[1]) - 1)]
