import random
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

print(randomSentence(5))