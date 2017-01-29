# usr/bin/env python
# -*- coding: utf-8 -*-


class LinkedQueue:

    class _Node:

        def __init__(self, element, next_node):
            self._element = element
            self._next = next_node

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Exception('The Queue is empty !')
        return self._head._element

    def dequeue(self):
        if self.is_empty():
            raise Exception('The Queue is empty !')
        the_element = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return the_element

    def enqueue(self, element):
        new_node = self._Node(element, None)
        if self.is_empty():
            self._head = new_node
        else:
            self._tail._next = new_node
        self._tail = new_node
        self._size += 1


class Tree:
    """Abstract base class representing a tree structure."""

    class Position:
        """An abstract representing the location of a single element."""

        def element(self):
            """Return the element stored at this position."""
            raise NotImplementedError('Must be implemented at subclass.')

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError('Must be implemented at subclass.')

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other)

    def root(self):
        """Return Position represents the tree's root."""
        raise NotImplementedError('Must be implementation at subclass.')

    def parent(self, p):
        """Return Position represents the p's parent( or None if p is root )."""
        raise NotImplementedError('Must be implemented at subclass.')

    def num_children(self, p):
        """Return the number of children that Position has."""
        raise NotImplementedError('Must be implemented at subclass.')

    def children(self, p):
        """Generate an iteration of Position representing p's children."""
        raise NotImplementedError('Must be implemented at subclass.')

    def __len__(self):
        """Return the total number of the elements in the tree."""
        raise NotImplementedError('Must be implemented at subclass.')

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.positions():
            yield p.element()

    def is_root(self, p):
        return self.root() == p

    def is_leaf(self, p):
        return self.num_children(p) == 0

    def is_empty(self):
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root():
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def height(self, p):
        """Return the height of the tree."""
        if self.is_leaf():
            return 0
        else:
            return 1 + max(self.height(c) for c in self.children(p))

    # -----------------------------preorder traversal--------------------------------
    def preorder(self):
        """Generate a preorder iteration of position in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.preorder()

    # -----------------------------postorder traversal--------------------------------
    def postorder(self):
        """Generate a postorder iteration of position in subtree rooted at p."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        """Generate an iteration of the tree's positions"""
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    # ------------------------------inorder traversal-----------------------------------
    def breadthfirst(self):
        """Generate a breadth-first iteration of the positions of the tree."""
        if not self.is_empty():
            fringe = LinkedQueue()


class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""

    def left(self, p):
        """Return a Position represents p's left child."""
        raise NotImplementedError('Must be implemented at subclass.')

    def right(self, p):
        raise NotImplementedError('Must be implemented at subclass.')

    def sibling(self, p):
        """Return a Position represents p's sibling( or None if no sibling )."""
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """Return a Position represents p's child( or children )."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):

        def __init__(self, container, node):
            """Constructor shouldn't be invoked by user."""
            self._container = container
            self._node = node

        @property
        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type.')
        if p._container is not self:
            raise ValueError('p does not belong to this container.')
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node( or None is not node )."""
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def add_root(self, element):
        """Place element element at the root of an
        empty tree and return new Position

        Raise ValueError if tree nonempty."""
        if self._root is not None:
            raise ValueError('Root exists.')
        self._size = 1
        self._root = self._Node(element)
        return self._make_position(self._root)

    def _add_left(self, p, element):
        """Create a new left child for Position p, storing element element.
        Return the Position of new node.

        Raise ValueError if Position is invalid of p already have a left child."""
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists.')
        self._size += 1
        node._left = self._Node(element, node)
        return self._make_position(node._left)

    def _add_right(self, p, element):
        """Create a new right child for Position p, storing element element.
        Return the Position of new node.

        Raise ValueError if Position is invalid of p already have a right child."""
        node = self._validate(p)
        if node._right() is not None:
            raise ValueError('Left child exists.')
        self._size += 1
        node._left = self._Node(element, node)
        return self._make_position(node._right)

    def _replace(self, p, element):
        """Replace the element at position p with element,
        and return old element."""
        node = self._validate(p)
        old = node._element
        node._element = element
        return old

    def delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any.
        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or has two children."""
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children.')
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('p must be leaf.')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must be much.')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2.size = 0

