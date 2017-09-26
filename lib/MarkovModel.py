from Dictogram import Dictogram


class MarkovModel:
    """ Basically a Markov Chain that generates sentences. """

    def __init__(self, corpus, order):
        """ Constructing the Markov Model

        :param corpus:      The file location of the corpus we want to use
        :param order:       The order for the Markov Chain
        """
        self.dictogram = Dictogram(corpus, order)

    def generate_sentence(self):
        """ Generates a sentence by first getting a sentence start then getting a random token following that word. We
        then end the sentence once we get to an end token ([NONE]). If the sentence is too small or too long we try
        generating a sentence gain.

        :return:    Our uniquely generated sentence
        """
        generated_sentence = ''

        # Our current element
        element = self.dictogram.data[self.dictogram.random_start()]

        # We could use a while loop, but we do this instead because we want to make sure we never get an infinite loop
        for _ in range(100):
            word = None

            # We get a new word or phrase
            current_word = element.random_word()

            # We make the new word or phrase our current element
            element = self.dictogram.data[current_word]

            # We only use the first word in the phrase
            word = " " + current_word.split(" ")[0]

            # If the word is a sentence end, we finish off the sentence.
            if word == " [NONE]":
                generated_sentence += "."
                break

            # Add current word to our new sentence
            generated_sentence += word

        # Remove the extra space in front of the sentence
        generated_sentence = generated_sentence[1:]

        sentence_length = len(generated_sentence)

        # If our sentence is too short or long we return a new sentence
        if sentence_length > 140 or sentence_length < 50:
            return self.generate_sentence()

        # Return our sentence and capitalize it. Also make sure there are no uncalled for None tokens
        return generated_sentence.capitalize().replace("[none]", "")


if __name__ == '__main__':
    model = MarkovModel("../public/test_data.txt", 3)

    print("Booted")

    for i in range(100):
        print(model.generate_sentence())
