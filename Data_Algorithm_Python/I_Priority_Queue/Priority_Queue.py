# usr/bin/env python
# -*- coding: utf-8 -*-


from Data_Algorithm_Python.G_Linked_List.Positional_List import PositionalList


class PriorityQueueBase(object):
    """Abstract base class for priority queue."""

    class _Item:
        """Lightweight composite to store priority queue items."""

        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key       # compare items based on their keys

    def is_empty(self):
        return len(self) == 0


class UnsortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implementation with unsorted list."""

    def __init__(self):
        self._data = PositionalList()

    def __len__(self):
        return len(self._data)

    def _find_min(self):
        if self.is_empty():
            raise Exception('Priority Queue is empty !')
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self._data.after(walk)
        return small

    def add(self, k, v):
        """Add a key-value pair."""
        self._data.add_last(self._Item(k, v))

    def min(self):
        """Return but don't remove (k, v) tuple with minimum key."""
        p = self._find_min()
        item = p.element()
        return item._key, item._value

    def remove_min(self):
        """Return and remove (k, v) tuple with minimum key."""
        p = self._find_min()
        item = self._data.delete(p)
        return item._key, item._value


class SortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a sorted list."""

    def __init__(self):
        """Create a new empty Priority Queue."""
        self._data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, k, v):
        """Add a key-value pair."""
        newest = self._Item(k, v)
        walk = self._data.last()    # walking backward looking for smaller key
        while walk is not None and newest < walk.element():
            walk = self._data.before(walk)
        if walk is None:
            self._data.add_first(newest)    # new key is smallest
        else:
            self._data.add_after(walk, newest)      # newest goes after walk

    def min(self):
        """Return but don't remove (k, v) tuple with minimum key."""
        if self.is_empty():
            raise Exception('Priority Queue is empty !')
        p = self._data.first()
        item = p.element()
        return item._key, item._value

    def remove_min(self):
        """Return and remove (k, v) tuple with minimum key."""
        if self.is_empty():
            raise Exception('Priority Queue is empty !')
        item = self._data.delete(self._data.first())
        return item._key, item._value


class HeapPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a binary heap."""

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    # --------------------------nonpublic behaviors-------------------------------
    def _parent(self, j):
        return (j-1)//2

    def _left(self, j):
        return 2*j+1

    def _right(self, j):
        return 2*j+2

    def _has_left(self, j):
        return self._left(j) < len(self._data)      # index beyond end of list ?

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """Swap the element at indices i and j of array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)        # recur at position parent

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    # ---------------------------public behaviors------------------------------------
    def add(self, key, value):
        """Add a key-value pair to the priority queue."""
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)       # upheap newly added position

    def min(self):
        """Return but not remove (key, value) tuple with minimum key.

        Raise Empty if empty."""
        if self.is_empty():
            raise Exception('Priority Queue is empty !')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        """Return and remove (key, value) tuple with minimum key.

        Raise Empty if empty"""
        if self.is_empty():
            raise Exception('Priority Queue is empty !')
        self._swap(0, len(self._data) - 1)      # put minimum item at the end
        item = self._data.pop()     # and remove it from the list
        self._downheap(0)       # then fix new root
        return item._key, item._value


class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    """A locator based priority queue implemented with a binary heap."""

    class Locator(HeapPriorityQueue._Item):
        """Token for locating an entry of the priority queue."""
        __slots__ = '_index'

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j

    # override swap to record indices
    def _swap(self, i, j):
        super()._swap(i, j)
        self._data[i]._index = i
        self._data[j]._index = j

    def _bubble(self, j):
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)

    def add(self, key, value):
        token = self.Locator(key, value, len(self._data))       # initialize locator index
        self._data.append(token)
        self._upheap(len(self._data)-1)
        return token

    def update(self, locator, new_key, new_value):
        """Update the key and value for the entry identified by Locator locator."""
        j = locator._index
        if not 0 <= j <=  len(self) and self._data[j] is locator:
            raise ValueError('invalid locator.')
        locator._key = new_key
        locator._value = new_value
        self._bubble(j)

    def remove(self, locator):
        j = locator._index
        if not 0 <= j <= len(self) and self._data[j] is locator:
            raise ValueError('invalid locator.')
        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j, len(self) - 1)
            self._data.pop()
            self._bubble(j)
        return locator._key, locator._value

