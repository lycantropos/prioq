import heapq
import sys
from functools import partial
from typing import (Generic,
                    List,
                    Optional,
                    Tuple)

from reprit.base import generate_repr

from .core.models import (ComplexItem,
                          ComplexReversedItem,
                          SimpleItem,
                          SimpleReversedItem)
from .hints import (Key,
                    SortingKey,
                    Value)


class PriorityQueue(Generic[Value]):
    """
    A priority queue is a mutable container
    that provides constant time lookup of the smallest (by default) element.

    Reference: https://en.wikipedia.org/wiki/Priority_queue
    """
    __slots__ = '_item_factory', '_items', '_key', '_reverse'

    def __init__(self, *values: Value,
                 key: Optional[SortingKey] = None,
                 reverse: bool = False) -> None:
        """
        Initializes queue.

        Complexity: O(log len(values)).

        :param values: initial values
        :param key: function of one argument to calculate priority.
        :param reverse:
            flag, if set to `True` specifies
            that values should be processed in descending order
            (from highest priority to lowest).

        >>> from prioq.base import PriorityQueue
        >>> values = range(-5, 5)
        >>> queue = PriorityQueue(*values, key=abs, reverse=True)
        >>> len(queue) == len(values)
        True
        >>> queue.key is abs
        True
        >>> queue.reverse
        True
        """
        self._item_factory = ((SimpleReversedItem
                               if reverse
                               else SimpleItem)
                              if key is None
                              else (partial(_to_complex_reversed_item, key)
                                    if reverse
                                    else partial(_to_complex_item, key)))
        self._items = [self._item_factory(value) for value in values]
        heapq.heapify(self._items)
        self._key = key
        self._reverse = reverse

    __repr__ = generate_repr(__init__)

    if sys.version_info < (3, 6, 4):
        # caused by https://github.com/python/typing/issues/498
        def __copy__(self) -> 'PriorityQueue[Value]':
            """
            Returns a shallow copy of the queue.

            Complexity: O(1).

            >>> queue = PriorityQueue(*range(5))
            >>> from copy import copy
            >>> copy(queue) == queue
            True
            """
            result = PriorityQueue(key=self._key,
                                   reverse=self._reverse)
            result._items = self._items
            return result

    def __eq__(self, other: 'PriorityQueue[Value]') -> bool:
        """
        Checks if the queue is equal to the given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue == PriorityQueue(*range(10))
        True
        >>> queue == PriorityQueue(*range(10), reverse=True)
        False
        >>> queue == PriorityQueue(*range(20))
        False
        >>> queue == PriorityQueue(*range(5))
        False
        """
        return (self is other
                or len(self) == len(other)
                and self.values() == other.values()
                if isinstance(other, PriorityQueue)
                else NotImplemented)

    def __len__(self) -> int:
        """
        Returns number of elements in the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(5))
        >>> len(queue)
        5
        """
        return len(self._items)

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    @property
    def reverse(self) -> bool:
        return self._reverse

    def clear(self) -> None:
        """
        Removes all values from the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(5))
        >>> queue.clear()
        >>> queue
        PriorityQueue(key=None, reverse=False)
        """
        self._items.clear()

    def peek(self) -> Value:
        """
        Returns front value of the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(5))
        >>> queue.peek()
        0
        >>> queue.push(-1)
        >>> queue.peek()
        -1
        >>> queue.push(0)
        >>> queue.peek()
        -1
        """
        try:
            return self._items[0].value
        except IndexError:
            raise ValueError('Priority queue is empty') from None

    def pop(self) -> Value:
        """
        Pops front value from the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(5))
        >>> queue.pop()
        0
        >>> queue
        PriorityQueue(1, 2, 3, 4, key=None, reverse=False)
        >>> queue.pop()
        1
        >>> queue
        PriorityQueue(2, 3, 4, key=None, reverse=False)
        """
        return heapq.heappop(self._items).value

    def push(self, value: Value) -> None:
        """
        Adds value to the queue.

        Complexity: O(log len(self)).

        >>> queue = PriorityQueue(*range(5))
        >>> queue.push(-1)
        >>> queue
        PriorityQueue(-1, 0, 1, 2, 3, 4, key=None, reverse=False)
        >>> queue.push(10)
        >>> queue
        PriorityQueue(-1, 0, 1, 2, 3, 4, 10, key=None, reverse=False)
        """
        heapq.heappush(self._items, self._item_factory(value))

    def remove(self, value: Value) -> None:
        """
        Removes value from the queue and if absent raises `ValueError`.

        Complexity: O(len(self)).

        >>> queue = PriorityQueue(*range(5))
        >>> queue.remove(0)
        >>> queue
        PriorityQueue(1, 2, 3, 4, key=None, reverse=False)
        >>> queue.remove(4)
        >>> queue
        PriorityQueue(1, 2, 3, key=None, reverse=False)
        """
        try:
            self._items.remove(self._item_factory(value))
        except ValueError:
            raise ValueError('{!r} is not in priority queue'
                             .format(value)) from None
        else:
            heapq.heapify(self._items)

    def values(self) -> List[Value]:
        """
        Returns elements of the queue.

        Complexity: O(len(self) * log len(self)).

        >>> queue = PriorityQueue(*range(5))
        >>> queue.values()
        [0, 1, 2, 3, 4]
        """
        return [item.value for item in sorted(self._items)]


def _to_complex_item(key: SortingKey, value: Value) -> ComplexItem:
    return ComplexItem(_to_pair(key, value))


def _to_complex_reversed_item(key: SortingKey,
                              value: Value) -> ComplexReversedItem:
    return ComplexReversedItem(_to_pair(key, value))


def _to_pair(key: SortingKey, value: Value) -> Tuple[Key, Value]:
    return key(value), value
