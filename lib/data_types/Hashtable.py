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

    def _get_bucket(self, key):
        bucket_number = hash(key) % len(self.buckets)
        return self.buckets[bucket_number]

    def contains(self, key):
        """Return True if this hash table contains the given key, or False"""
        bucket_number = hash(key) % len(self.buckets)
        bucket = self.buckets[bucket_number]

        current = bucket.head
        while current is not None:
            if current.data[0] == key:
                return True

            current = current.next

        return False

    def get(self, key):
        """Return the value associated with the given key, or raise KeyError"""
        bucket_number = hash(key) % len(self.buckets)
        bucket = self.buckets[bucket_number]

        current = bucket.head
        while current is not None:
            if current.data[0] == key:
                return current.data[1]

            current = current.next

        raise KeyError

    def set(self, key, value):
        """Insert or update the given key with its associated value"""
        bucket_number = hash(key) % len(self.buckets)
        bucket = self.buckets[bucket_number]

        current = bucket.head
        while current is not None:
            if current.data[0] == key:
                current.data = (key, value)
                return

            current = current.next

        bucket.append((key, value))

    def delete(self, key):
        if not self.contains(key):
            raise KeyError

        bucket_number = hash(key) % len(self.buckets)
        bucket = self.buckets[bucket_number]

        last = None
        current = bucket.head
        while current is not None:
            if current.data[0] == key:
                if bucket.tail.data[0] == key:
                    bucket.tail = last

                if last is None:
                    bucket.head = current.next
                else:
                    last.next = current.next

                return

            current = current.next

        raise KeyError


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