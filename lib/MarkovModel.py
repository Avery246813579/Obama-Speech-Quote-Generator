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
        self.dictogram = Dictogram(self.parser.words, order)
        # self.back = Dictogram(reversed(parser.words), ror)

    def generate_sentence(self, backward=False):
        """ Generates a sentence by first getting a sentence start then getting a random token following that word. We
        then end the sentence once we get to an end token ([NONE]). If the sentence is too small or too long we try
        generating a sentence gain.

        :return:    Our uniquely generated sentence
        """

        element = None
        generated_sentence = ''

        if backward:
            window = deque(self.dictogram.random_start(True))
            element = self.dictogram.backwards[tuple(window)]
            generated_sentence = ' '.join(list(reversed(window)))
        else:
            window = deque(self.dictogram.random_start(False))
            element = self.dictogram.forwards[tuple(window)]
            generated_sentence = ' '.join(window)

        # If the window has a split
        if '[SPLIT]' in generated_sentence:
            return self.generate_sentence(backward)

        # We could use a while loop, but we do this instead because we want to make sure we never get an infinite loop
        for _ in range(self.MAX_ITERATION_ATTEMPTS):
            word = None

            # We get a new word or phrase
            current_word = element.random_word()

            # If the word is a sentence end, we finish off the sentence.
            if current_word == '[SPLIT]':
                if not backward:
                    generated_sentence += '.'

                break

            # We make the new word or phrase our current element
            window.popleft()
            window.append(current_word)

            if backward:
                element = self.dictogram.backwards[tuple(window)]

                # We only use the first word in the phrase
                word = current_word + " "

                # Add current word to our new sentence
                generated_sentence = word + generated_sentence
            else:
                element = self.dictogram.forwards[tuple(window)]

                word = " " + current_word

                generated_sentence += word

        sentence_length = len(generated_sentence)

        # If our sentence is too short or long we return a new sentence
        if sentence_length > self.MAX_TWEET_LENGTH or sentence_length < self.MIN_TWEET_LENGTH:
            return self.generate_sentence(backward)

        # Return our sentence and capitalize it. Also make sure there are no uncalled for None tokens
        return generated_sentence

    def generate_with_seed(self, raw_seed):
        seed = tuple(raw_seed.split())

        if seed in self.dictogram.forwards and tuple(reversed(seed)) in self.dictogram.backwards:
            forward_element = self.dictogram.forwards[seed]
            forward_window = deque(seed)
            forward_sentence = ''

            for _ in range(self.MAX_ITERATION_ATTEMPTS):
                word = None

                # We get a new word or phrase
                current_word = forward_element.random_word()

                # If the word is a sentence end, we finish off the sentence.
                if current_word == '[SPLIT]':
                    forward_sentence += '.'
                    break

                # We make the new word or phrase our current element
                forward_window.popleft()
                forward_window.append(current_word)

                forward_element = self.dictogram.forwards[tuple(forward_window)]
                word = " " + current_word
                forward_sentence += word

            forward_length = len(forward_sentence)

            # If our sentence is too short or long we return a new sentence
            if forward_length > self.MAX_TWEET_LENGTH / 2 or forward_length < self.MIN_TWEET_LENGTH / 2:
                return self.generate_with_seed(raw_seed)

            backward_window = deque(tuple(reversed(seed)))
            backward_element = self.dictogram.backwards[tuple(reversed(seed))]
            backward_sentence = ' '.join(list(reversed(backward_window)))

            # If the window has a split
            if '[SPLIT]' in backward_sentence:
                return self.generate_with_seed(raw_seed)

            for _ in range(self.MAX_ITERATION_ATTEMPTS):
                word = None

                # We get a new word or phrase
                current_word = backward_element.random_word()

                # If the word is a sentence end, we finish off the sentence.
                if current_word == '[SPLIT]':
                    break

                # We make the new word or phrase our current element
                backward_window.popleft()
                backward_window.append(current_word)

                backward_element = self.dictogram.backwards[tuple(backward_window)]
                word = current_word + " "
                backward_sentence = word + backward_sentence

            backward_length = len(backward_sentence)

            # If our sentence is too short or long we return a new sentence
            if backward_length > self.MAX_TWEET_LENGTH / 2 or backward_length < self.MIN_TWEET_LENGTH / 2:
                return self.generate_with_seed(raw_seed)

            print(backward_sentence + forward_sentence)

            return True
        else:
            return False


if __name__ == '__main__':
    model = MarkovModel("static/test_data.txt", 3)

    print("Booted")

    print("FORWARD:")
    for i in range(10):
        print(model.generate_sentence())

    print("BACKWARD:")
    for i in range(10):
        print(model.generate_sentence(True))

    print("\n\n\n")

    print(model.generate_with_seed('that makes us'))
