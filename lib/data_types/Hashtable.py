#!python

from data_types.LinkedList import LinkedList


class HashTable(object):

    def __init__(self, init_size=8):
        """Initialize this hash table with the given initial size"""
        self.buckets = [LinkedList() for i in range(init_size)]

    def __str__(self):
        """Return a formatted string representation of this hash table"""
        items = ['{}: {}'.format(repr(k), repr(v)) for k, v in self.items()]
        return '{' + ', '.join(items) + '}'

    def __repr__(self):
        """Return a string representation of this hash table"""
        return 'HashTable({})'.format(repr(self.items()))

    def _bucket_index(self, key):
        """Return the bucket index where the given key would be stored"""
        return hash(key) % len(self.buckets)

    def keys(self):
        """Return a list of all keys in this hash table"""
        # Collect all keys in each of the buckets
        all_keys = []
        for bucket in self.buckets:
            for key, value in bucket.items():
                all_keys.append(key)
        return all_keys

    def values(self):
        """Return a list of all values in this hash table"""
        values = []

        for item in self.items():
            values.append(item[1])

        return values

    def items(self):
        """Return a list of all items (key-value pairs) in this hash table"""
        # Collect all pairs of key-value entries in each of the buckets
        all_items = []
        for bucket in self.buckets:
            all_items.extend(bucket.items())
        return all_items

    def length(self):
        """Return the length of this hash table by traversing its buckets"""
        length = 0
        for bucket in self.buckets:
            length += bucket.length()

        return length

    def _find_bucket(self, key):
        bucket_number = hash(key) % len(self.buckets)
        return self.buckets[bucket_number]

    def _find_node(self, key):
        bucket = self._find_bucket(key)

        current = bucket.head
        while current is not None:
            if current.data[0] == key:
                return current

            current = current.next

    def contains(self, key):
        """Return True if this hash table contains the given key, or False"""
        return self._find_node(key) is not None

    def get(self, key):
        """Return the value associated with the given key, or raise KeyError"""
        node = self._find_node(key)

        if node is None:
            raise KeyError

        return node.data[1]

    def set(self, key, value):
        """Insert or update the given key with its associated value"""
        node = self._find_node(key)

        if node is None:
            self._find_bucket(key).append((key, value))
            return

        node.data = (key, value)

    def delete(self, key):
        node = self._find_node(key)

        if self._find_node(key) is None:
            raise KeyError

        self._find_bucket(key).delete(node.data)


def test_hash_table():
    ht = HashTable()
    print(ht)

    print('Setting entries:')
    ht.set('I', 1)
    print(ht)
    ht.set('V', 5)
    print(ht)
    ht.set('X', 10)
    print(ht)
    print('contains(X): ' + str(ht.contains('X')))
    print('get(I): ' + str(ht.get('I')))
    print('get(V): ' + str(ht.get('V')))
    print('get(X): ' + str(ht.get('X')))
    print('length: ' + str(ht.length()))

    # Enable this after implementing delete:
    # print('Deleting entries:')
    # ht.delete('I')
    # print(ht)
    # ht.delete('V')
    # print(ht)
    # ht.delete('X')
    # print(ht)
    # print('contains(X): ' + str(ht.contains('X')))
    # print('length: ' + str(ht.length()))


if __name__ == '__main__':
    test_hash_table()