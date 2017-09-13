class Tree:
    def __init__(self, value):
        self.head = Node(value)

    def __str__(self):
        return str(self.head)

class Node:
    def __init__(self, value):
        self.count = 1
        self.value = "Dog"
        self.children = []

    def __str__(self):
        return str()



if __name__ == '__main__':
    print("Test")