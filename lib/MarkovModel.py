from Dictogram import Dictogram


class MarkovModel:
    def __init__(self, corpus, order):
        self.map_gram = Dictogram(corpus, order)

    def generate_sentence(self, length):
        to_return = ''

        element = None
        for i in range(length):
            word = None

            if element is None:
                word = self.map_gram.random_key()
                element = self.map_gram.data[word]
                word = " " + word.split(" ")[0]
            else:
                word = element.random_word()

                if word == "[NONE]":
                    word = self.map_gram.random_key()
                    element = self.map_gram.data[word]
                    word = ". " + word.split(" ")[0]
                else:
                    element = self.map_gram.data[word]
                    word = " " + word.split(" ")[0]

            to_return += word

        return to_return[1:].capitalize()

    def __str__(self):
        return str()

if __name__ == '__main__':
    model = MarkovModel("static/test_data.txt", 3)

    print("Booted")
    print(model.generate_sentence(20))
    print("Booted")
    print(model.generate_sentence(20))
