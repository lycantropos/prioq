import heapq
import sys
from functools import partial
from operator import (attrgetter,
                      itemgetter)
from typing import (Generic,
                    Iterator,
                    MutableSet,
                    Optional,
                    Sequence,
                    Tuple)

from reprit.base import generate_repr

from .hints import (Domain,
                    Key,
                    OtherDomain,
                    Range)
from .reversing import (ComplexReverser,
                        SimpleReverser)
from .utils import identity


def reverse_key(key: Optional[Key]) -> Key:
    return (SimpleReverser
            if key is None
            else partial(_to_complex_reverser, key))


def _to_complex_reverser(key: Key, value: Domain) -> ComplexReverser:
    return ComplexReverser(_to_item(key, value))


def _to_item(key: Key, value: Domain) -> Tuple[Range, Domain]:
    return key(value), value


@MutableSet.register
class PriorityQueue(Generic[Domain]):
    """
    A priority queue is a mutable container
    that provides constant time lookup of the smallest (by default) element.

    Reference: https://en.wikipedia.org/wiki/Priority_queue
    """
    __slots__ = ('_key', '_reverse', '_items',
                 '_item_to_value', '_value_to_item')

    def __init__(self, *_values: Domain,
                 key: Optional[Key] = None,
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
        >>> values = range(-5, 6)
        >>> queue = PriorityQueue(*values, key=abs, reverse=True)
        >>> all(value in queue for value in values)
        True
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

    if sys.version_info < (3, 6):
        # caused by https://github.com/python/typing/issues/498
        def __copy__(self) -> 'PriorityQueue[Domain]':
            """
            Returns a shallow copy of the queue.

            Complexity: O(1).
            """
            result = PriorityQueue(key=self._key,
                                   reverse=self._reverse)
            result._items = self._items
            return result

    @property
    def _values(self) -> Sequence[Domain]:
        return [self._item_to_value(item) for item in self._items]

    @property
    def reverse(self) -> bool:
        return self._reverse

    @property
    def key(self) -> Optional[Key]:
        return self._key

    def __contains__(self, value: Domain) -> bool:
        """
        Checks if value is present in the queue.

        Complexity: O(len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> 0 in queue
        True
        >>> -1 in queue
        False
        """
        return value in self._values

    def __eq__(self, other: 'PriorityQueue[OtherDomain]') -> bool:
        """
        Checks if the queue is equal to the given one.

        Complexity: O(len(self) * log len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue == PriorityQueue(*range(10))
        True
        >>> queue == PriorityQueue(*range(10), reverse=True)
        True
        >>> queue == PriorityQueue(*range(20))
        False
        >>> queue == PriorityQueue(*range(5))
        False
        """
        return (len(self) == len(other)
                and all(value == other_value
                        for value, other_value in zip(self, other))
                if isinstance(other, PriorityQueue)
                else NotImplemented)

    def __len__(self) -> int:
        """
        Returns number of elements in the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(10))
        >>> len(queue)
        10
        """
        return len(self._items)

    def __iter__(self) -> Iterator[Domain]:
        """
        Iterates over the queue in sorted order.

        Complexity: O(len(self) * log len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(queue)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        self._items = sorted(self._items)
        return iter(self._values)

    def __reversed__(self) -> Iterator[Domain]:
        """
        Iterates over the queue in reversed order.

        Complexity: O(len(self) * log len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(reversed(queue))
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        """
        return iter(sorted(self._values,
                           key=self._key,
                           reverse=not self._reverse))

    def add(self, value: Domain) -> None:
        """
        Adds value to the queue.

        Complexity: O(log len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue.add(-1)
        >>> list(queue)
        [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> queue.add(0)
        >>> list(queue)
        [-1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        heapq.heappush(self._items, self._value_to_item(value))

    def discard(self, value: Domain) -> None:
        """
        Removes value from the queue if present.

        Complexity: O(len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue.discard(-1)
        >>> list(queue)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> queue.discard(0)
        >>> list(queue)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        try:
            self._items.remove(self._value_to_item(value))
        except ValueError:
            pass
        else:
            heapq.heapify(self._items)

    def peek(self) -> Domain:
        """
        Returns front value of the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(10))
        >>> queue.peek()
        0
        >>> queue.add(-1)
        >>> queue.peek()
        -1
        >>> queue.add(0)
        >>> queue.peek()
        -1
        """
        try:
            return self._item_to_value(self._items[0])
        except IndexError:
            raise KeyError

    def pop(self) -> Domain:
        """
        Pops front value from the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(10))
        >>> queue.pop()
        0
        >>> list(queue)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> queue.pop()
        1
        >>> list(queue)
        [2, 3, 4, 5, 6, 7, 8, 9]
        """
        try:
            return self._item_to_value(heapq.heappop(self._items))
        except IndexError:
            raise KeyError

    def clear(self) -> None:
        """
        Removes all values from the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(10))
        >>> queue.clear()
        >>> list(queue)
        []
        """
        self._items.clear()
