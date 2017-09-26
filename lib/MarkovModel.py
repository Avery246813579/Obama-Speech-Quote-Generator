from Dictogram import Dictogram


class MarkovModel:
    """ Basically a Markov Chain that generates sentences """

    def __init__(self, corpus, order):
        self.map_gram = Dictogram(corpus, order)

    def generate_sentence(self, length):
        to_return = ''

        element = None
        for i in range(100):
            word = None

            if element is None:
                element = self.map_gram.data[self.map_gram.random_start()]

                word = element.random_word()
                element = self.map_gram.data[word]
                word = " " + word.split(" ")[0]
            else:
                current_word = element.random_word()

                if current_word == "[NONE]":
                    current_word = self.map_gram.random_key()
                    element = self.map_gram.data[current_word]
                    word = ". " + current_word.split(" ")[0]
                else:
                    element = self.map_gram.data[current_word]
                    word = " " + current_word.split(" ")[0]

            if word == " [NONE]":
                to_return += "."
                break

            to_return += word

        if len(to_return[1:]) > 140 or len(to_return[1:]) < 50:
            return self.generate_sentence(length)

        return to_return[1:].capitalize().replace("[none]", "")

    def __str__(self):
        return str()


if __name__ == '__main__':
    model = MarkovModel("../public/test_data.txt", 3)

    print("Booted")
    print(model.generate_sentence(20))
    print("Booted")
    print(model.generate_sentence(20))
