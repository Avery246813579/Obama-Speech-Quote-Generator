from RainbowChain import Dictogram
from collections import deque


class RainbowChain:
    """ Basically a Markov Chain that generates sentences. """

    # Max amount of attempts we have to generate a new sentence
    MAX_ITERATION_ATTEMPTS = 100

    def __init__(self, corpus, max_order):
        """ Constructing the Markov Model

        :param corpus:      The file location of the corpus we want to use
        :param order:       The order for the Markov Chain
        """

        self.parser = FileParser(corpus)
        self.dictogram = []
        self.max_order = max_order

        for order in range(1, max_order + 1):
            print("START: " + str(order))
            self.dictogram.append(Dictogram(self.parser.words, order))
            print("END: " + str(order))


    def generate_sentence(self, backward=False, min_length=50, max_length=140):
        """ Generates a sentence by first getting a sentence start then getting a random token following that word. We
        then end the sentence once we get to an end token ([NONE]). If the sentence is too small or too long we try
        generating a sentence gain.

        :return:    Our uniquely generated sentence
        """

        element = None
        generated_sentence = ''

        if backward:
            window = deque(self.dictogram[self.max_order - 1].random_start(True))
            element = self.dictogram[self.max_order - 1].backwards[tuple(window)]
            generated_sentence = ' '.join(list(reversed(window)))
        else:
            window = deque(self.dictogram[self.max_order - 1].random_start(False))
            element = self.dictogram[self.max_order - 1].forwards[tuple(window)]
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
                element = self.dictogram[self.max_order - 1].backwards[tuple(window)]

                # We only use the first word in the phrase
                word = current_word + " "

                # Add current word to our new sentence
                generated_sentence = word + generated_sentence
            else:
                element = self.dictogram[self.max_order - 1].forwards[tuple(window)]

                word = " " + current_word

                generated_sentence += word

        sentence_length = len(generated_sentence)

        # If our sentence is too short or long we return a new sentence
        if sentence_length > max_length or sentence_length < min_length:
            return self.generate_sentence(backward)

        # If we are backwards add a period at the end of a sentence
        if backward:
            generated_sentence += '.'

        # Return our sentence and capitalize it. Also make sure there are no uncalled for None tokens
        return generated_sentence

    def generate_with_seed(self, raw_seed, min_length=50, max_length=140, depth=0):
        seed = list(raw_seed.split())

        while len(seed) < self.max_order:
            try:
                word = self.dictogram[len(seed) - 1].forwards[tuple(seed)].random_word()

                if word == '[SPLIT]':
                    return self.generate_with_seed(raw_seed)

                seed.append(word)
            except KeyError:
                return None

        seed = tuple(seed)

        if seed in self.dictogram[self.max_order - 1].forwards and tuple(reversed(seed)) in self.dictogram[
                    self.max_order - 1].backwards:
            forward_element = self.dictogram[self.max_order - 1].forwards[seed]
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

                forward_element = self.dictogram[self.max_order - 1].forwards[tuple(forward_window)]
                word = " " + current_word
                forward_sentence += word

            forward_length = len(forward_sentence)

            # If our sentence is too short or long we return a new sentence
            if forward_length > max_length / 2 or forward_length < min_length / 2:
                if depth > self.MAX_ITERATION_ATTEMPTS:
                    return None

                return self.generate_with_seed(raw_seed, depth=depth + 1)

            backward_window = deque(tuple(reversed(seed)))
            backward_element = self.dictogram[self.max_order - 1].backwards[tuple(reversed(seed))]
            backward_sentence = ' '.join(list(reversed(backward_window)))

            # If the window has a split
            if '[SPLIT]' in backward_sentence:
                if depth > self.MAX_ITERATION_ATTEMPTS:
                    return None

                return self.generate_with_seed(raw_seed, depth=depth + 1)

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

                backward_element = self.dictogram[self.max_order - 1].backwards[tuple(backward_window)]
                word = current_word + " "
                backward_sentence = word + backward_sentence

            backward_length = len(backward_sentence)

            # If our sentence is too short or long we return a new sentence
            if backward_length > max_length / 2 or backward_length < min_length / 2:
                if depth > self.MAX_ITERATION_ATTEMPTS:
                    return None

                return self.generate_with_seed(raw_seed, depth=depth + 1)

            return backward_sentence + forward_sentence



class FileParser:
    """ FileParser is a class used to parse both lines and words from a file. I will also sterilize the data """

    # TODO: When cleaning lines. Check that it's not a whitelisted use of a period

    def __init__(self, file_name):
        """ We read a file named :file_name: and put all of the words and lines into a variable
        :param file_name:       The name of the file we want to parse
        """

        file_reader = open(file_name, "r", encoding="utf8")

        self.words = []
        self.lines = file_reader.read().splitlines()

        # Goes through all the lines, cleans them, then splits it up into words and adds them to the words variable
        for line in self.lines:
            self.words += line.split()

    @staticmethod
    def clean_line(line):
        """ We clean a line. At the moment we just add the [NONE] token at the end of sentences.
        :param line:    The line we want to clean
        :return:        The cleaned line
        """

        return line.replace('.', ' [NONE]')
