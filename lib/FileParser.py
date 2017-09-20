class FileParser:
    def __init__(self, file):
        file = open(file, "r")
        self.lines = file.read().splitlines()

        self.words = []
        for i in range(len(self.lines)):
            self.words += self.lines[i].split()
