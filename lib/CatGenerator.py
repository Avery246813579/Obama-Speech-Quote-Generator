import random


def smart_shuffle(lst):
    for i in range(len(lst)):
        index = random.randint(i, len(lst) - 1)
        item = lst[index]
        lst[index] = lst[i]
        lst[i] = item


if __name__ == '__main__':
    argz = ["Test", "Dog", "cat"]

    smart_shuffle(argz)

    print(argz)