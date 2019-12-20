import heapq
import sys
from functools import partial
from operator import (attrgetter,
                      itemgetter)
from typing import (Generic,
                    Optional,
                    Sequence,
                    Tuple)

from reprit.base import generate_repr

from .hints import (Key,
                    SortingKey,
                    Value)
from .reversing import (ComplexReverser,
                        SimpleReverser)
from .utils import identity


def reverse_key(key: Optional[SortingKey]) -> SortingKey:
    return (SimpleReverser
            if key is None
            else partial(_to_complex_reverser, key))


def _to_complex_reverser(key: SortingKey, value: Value) -> ComplexReverser:
    return ComplexReverser(_to_item(key, value))


def _to_item(key: SortingKey, value: Value) -> Tuple[Key, Value]:
    return key(value), value


class PriorityQueue(Generic[Value]):
    """
    A priority queue is a mutable container
    that provides constant time lookup of the smallest (by default) element.

    Reference: https://en.wikipedia.org/wiki/Priority_queue
    """
    __slots__ = ('_key', '_reverse', '_items',
                 '_item_to_value', '_value_to_item')

    def __init__(self, *_values: Value,
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
        >>> queue.key is abs
        True
        >>> queue.reverse
        True
        """
        self._key = key
        self._reverse = reverse
        self._value_to_item = (reverse_key(key)
                               if reverse
                               else (identity if key is None
                                     else partial(_to_item, key)))
        self._item_to_value = (attrgetter('value')
                               if reverse
                               else (identity if key is None
                                     else itemgetter(1)))
        self._items = [self._value_to_item(value) for value in _values]
        heapq.heapify(self._items)

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

    @property
    def _values(self) -> Sequence[Value]:
        return [self._item_to_value(item) for item in sorted(self._items)]

    @property
    def reverse(self) -> bool:
        return self._reverse

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    def __len__(self) -> int:
        """
        Returns number of elements in the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(5))
        >>> len(queue)
        5
        """
        return len(self._items)

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
                and self._values == other._values
                if isinstance(other, PriorityQueue)
                else NotImplemented)

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
        heapq.heappush(self._items, self._value_to_item(value))

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
            self._items.remove(self._value_to_item(value))
        except ValueError:
            raise ValueError(value)
        else:
            heapq.heapify(self._items)

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
            return self._item_to_value(self._items[0])
        except IndexError:
            raise KeyError

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
        return self._item_to_value(heapq.heappop(self._items))

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
