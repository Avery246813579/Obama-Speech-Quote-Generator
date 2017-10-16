from Dictogram import Dictogram
from collections import deque
from FileParser import FileParser

class MarkovModel:
    """ Basically a Markov Chain that generates sentences. """

    # Maximum amount of characters we allow our sentence to have
    MAX_TWEET_LENGTH = 140

    # Minimum amount of characters we allow our sentence to have
    MIN_TWEET_LENGTH = 50

    # Max amount of attempts we have to generate a new sentence
    MAX_ITERATION_ATTEMPTS = 100

    def __init__(self, corpus, order):
        """ Constructing the Markov Model

        :param corpus:      The file location of the corpus we want to use
        :param order:       The order for the Markov Chain
        """

        self.parser = FileParser(corpus)
        self.dictogram = Dictogram(list(reversed(self.parser.words)), order)
        # self.back = Dictogram(reversed(parser.words), ror)

    def generate_sentence(self):
        """ Generates a sentence by first getting a sentence start then getting a random token following that word. We
        then end the sentence once we get to an end token ([NONE]). If the sentence is too small or too long we try
        generating a sentence gain.

        :return:    Our uniquely generated sentence
        """

        # Our current element
        window = deque(self.dictogram.random_start())
        element = self.dictogram.data[tuple(window)]
        generated_sentence = ' '.join(list(reversed(window)))

        print(window)

        # If the window has a split
        if '[SPLIT]' in generated_sentence:
            return self.generate_sentence()

        # We could use a while loop, but we do this instead because we want to make sure we never get an infinite loop
        for _ in range(self.MAX_ITERATION_ATTEMPTS):
            word = None

            # We get a new word or phrase
            current_word = element.random_word()

            # If the word is a sentence end, we finish off the sentence.
            if current_word == '[SPLIT]':
                print(window)
                break

            # We make the new word or phrase our current element
            window.popleft()
            window.append(current_word)
            element = self.dictogram.data[tuple(window)]

            # We only use the first word in the phrase
            word = current_word + " "

            # Add current word to our new sentence
            generated_sentence = word + generated_sentence

        sentence_length = len(generated_sentence)

        # If our sentence is too short or long we return a new sentence
        if sentence_length > self.MAX_TWEET_LENGTH or sentence_length < self.MIN_TWEET_LENGTH:
            return self.generate_sentence()

        # Return our sentence and capitalize it. Also make sure there are no uncalled for None tokens
        return generated_sentence


if __name__ == '__main__':
    model = MarkovModel("static/test_data.txt", 3)

    print("Booted")

    for i in range(1):
        print(model.generate_sentence())
