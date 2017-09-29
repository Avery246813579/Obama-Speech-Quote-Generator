file = open("/usr/share/dict/words", "r")
words = file.read().splitlines()

for word in words:
    if word[::-1] in words:
        print(word, word[::-1])