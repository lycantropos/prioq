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

from .hints import (Key,
                    SortingKey,
                    Value)
from .reversing import (ComplexReverser,
                        SimpleReverser)
from .utils import (identity,
                    intersect_sorted,
                    subtract_sorted)


def reverse_key(key: Optional[SortingKey]) -> SortingKey:
    return (SimpleReverser
            if key is None
            else partial(_to_complex_reverser, key))


def _to_complex_reverser(key: SortingKey, value: Value) -> ComplexReverser:
    return ComplexReverser(_to_item(key, value))


def _to_item(key: SortingKey, value: Value) -> Tuple[Key, Value]:
    return key(value), value


@MutableSet.register
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

    if sys.version_info < (3, 6, 4):
        # caused by https://github.com/python/typing/issues/498
        def __copy__(self) -> 'PriorityQueue[Value]':
            """
            Returns a shallow copy of the queue.

            Complexity: O(1).

            >>> queue = PriorityQueue(*range(10))
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
        return [self._item_to_value(item) for item in self._items]

    @property
    def reverse(self) -> bool:
        return self._reverse

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    def __contains__(self, value: Value) -> bool:
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

    def __len__(self) -> int:
        """
        Returns number of elements in the queue.

        Complexity: O(1).

        >>> queue = PriorityQueue(*range(10))
        >>> len(queue)
        10
        """
        return len(self._items)

    def __iter__(self) -> Iterator[Value]:
        """
        Iterates over the queue in sorted order.

        Complexity: O(len(self) * log len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(queue)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        self._items = sorted(self._items)
        return iter(self._values)

    def __reversed__(self) -> Iterator[Value]:
        """
        Iterates over the queue in reversed order.

        Complexity: O(len(self) * log len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(reversed(queue))
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        """
        self._items = sorted(self._items)
        return iter(self._values[::-1])

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
        return (self is other or self <= other <= self
                if isinstance(other, PriorityQueue)
                else NotImplemented)

    def __ge__(self, other: 'PriorityQueue[Value]') -> bool:
        """
        Checks if the queue is a superset of given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue >= PriorityQueue(*range(10))
        True
        >>> queue >= PriorityQueue(*range(10), reverse=True)
        False
        >>> queue >= PriorityQueue(*range(20))
        False
        >>> queue >= PriorityQueue(*range(5))
        True
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        if self is other:
            return True
        elif len(self) < len(other):
            return False
        else:
            values, other_values = iter(self), iter(other)
            return all(value in values for value in other_values)

    def __gt__(self, other: 'PriorityQueue[Value]') -> bool:
        """
        Checks if the queue is a strict superset of given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue > PriorityQueue(*range(10))
        False
        >>> queue > PriorityQueue(*range(10), reverse=True)
        False
        >>> queue > PriorityQueue(*range(20))
        False
        >>> queue > PriorityQueue(*range(5))
        True
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        return len(self) > len(other) and self >= other and self != other

    def __le__(self, other: 'PriorityQueue[Value]') -> bool:
        """
        Checks if the queue is a subset of given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue <= PriorityQueue(*range(10))
        True
        >>> queue <= PriorityQueue(*range(10), reverse=True)
        False
        >>> queue <= PriorityQueue(*range(20))
        True
        >>> queue <= PriorityQueue(*range(5))
        False
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        if self is other:
            return True
        elif len(self) > len(other):
            return False
        else:
            values, other_values = iter(self), iter(other)
            return all(value in other_values for value in values)

    def __lt__(self, other: 'PriorityQueue[Value]') -> bool:
        """
        Checks if the queue is a strict subset of given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue < PriorityQueue(*range(10))
        False
        >>> queue < PriorityQueue(*range(10), reverse=True)
        False
        >>> queue < PriorityQueue(*range(20))
        True
        >>> queue < PriorityQueue(*range(5))
        False
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        return len(self) < len(other) and self <= other and self != other

    def __and__(self, other: 'PriorityQueue[Value]') -> 'PriorityQueue[Value]':
        """
        Returns intersection of the queue with given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(queue & PriorityQueue(*range(10)))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> list(queue & PriorityQueue(*range(10), reverse=True))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> list(queue & PriorityQueue(*range(20)))
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> list(queue & PriorityQueue(*range(5)))
        [0, 1, 2, 3, 4]
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        if self._key is other._key:
            other_values = list(other
                                if self._reverse is other._reverse
                                else reversed(other))
        else:
            other_values = sorted(other._values,
                                  key=self._key,
                                  reverse=self._reverse)
        return PriorityQueue(*intersect_sorted(list(self), other_values,
                                               key=self._key,
                                               reverse=self._reverse),
                             key=self._key,
                             reverse=self._reverse)

    def __or__(self, other: 'PriorityQueue[Value]') -> 'PriorityQueue[Value]':
        """
        Returns union of the queue with given one.

        Complexity: O(len(self) + len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(queue | PriorityQueue(*range(10)))
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        >>> list(queue | PriorityQueue(*range(10), reverse=True))
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        >>> list(queue | PriorityQueue(*range(5)))
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 9]
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        return PriorityQueue(*self._values, *other._values,
                             key=self._key,
                             reverse=self._reverse)

    def __sub__(self, other: 'PriorityQueue[Value]') -> 'PriorityQueue[Value]':
        """
        Returns subtraction of the queue with given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(queue - PriorityQueue(*range(10)))
        []
        >>> list(queue - PriorityQueue(*range(10), reverse=True))
        []
        >>> list(queue - PriorityQueue(*range(20)))
        []
        >>> list(queue - PriorityQueue(*range(5)))
        [5, 6, 7, 8, 9]
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        if self._key is other._key:
            other_values = list(other
                                if self._reverse is other._reverse
                                else reversed(other))
        else:
            other_values = sorted(other._values,
                                  key=self._key,
                                  reverse=self._reverse)
        return PriorityQueue(*subtract_sorted(list(self), other_values,
                                              key=self._key,
                                              reverse=self._reverse),
                             key=self._key,
                             reverse=self._reverse)

    def __xor__(self, other: 'PriorityQueue[Value]') -> 'PriorityQueue[Value]':
        """
        Returns symmetric difference of the queue with given one.

        Complexity: O(len(self) * log len(self) + len(other) * log len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> list(queue ^ PriorityQueue(*range(10)))
        []
        >>> list(queue ^ PriorityQueue(*range(10), reverse=True))
        []
        >>> list(queue ^ PriorityQueue(*range(20)))
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        >>> list(queue ^ PriorityQueue(*range(5)))
        [5, 6, 7, 8, 9]
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        if not self:
            return other
        elif not other:
            return self
        else:
            return (self - other) | (other - self)

    def __iand__(self, other: 'PriorityQueue[Value]'
                 ) -> 'PriorityQueue[Value]':
        """
        Intersects the queue with given one in-place.

        Complexity: O(len(self) * len(other)).
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        self._items = (self & other)._items
        return self

    def __ior__(self, other: 'PriorityQueue[Value]') -> 'PriorityQueue[Value]':
        """
        Unites the queue with given one in-place.

        Complexity: O(len(self) + len(other)).
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        self._items = (self | other)._items
        return self

    def __ixor__(self, other: 'PriorityQueue[Value]'
                 ) -> 'PriorityQueue[Value]':
        """
        Exclusively disjoins the queue with given one in-place.

        Complexity: O(len(self) * len(other)).
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        self._items = (self ^ other)._items
        return self

    def __isub__(self, other: 'PriorityQueue[Value]'
                 ) -> 'PriorityQueue[Value]':
        """
        Subtracts from the queue a given one in-place.

        Complexity: O(len(self) * len(other))
        """
        if not isinstance(other, PriorityQueue):
            return NotImplemented
        self._items = (self - other)._items
        return self

    def isdisjoint(self, other: 'PriorityQueue[Value]') -> bool:
        """
        Checks if the queue has no intersection with given one.

        Complexity: O(len(self) * len(other)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue.isdisjoint(PriorityQueue(*range(10)))
        False
        >>> queue.isdisjoint(PriorityQueue(*range(10), reverse=True))
        False
        >>> queue.isdisjoint(PriorityQueue(*range(20)))
        False
        >>> queue.isdisjoint(PriorityQueue(*range(5)))
        False
        """
        other_values = other._values
        return all(value not in other_values for value in self._values)

    def add(self, value: Value) -> None:
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

    def remove(self, value: Value) -> None:
        """
        Removes value from the queue and if absent raises `KeyError`.

        Complexity: O(len(self)).

        >>> queue = PriorityQueue(*range(10))
        >>> queue.remove(0)
        >>> list(queue)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> queue.remove(9)
        >>> list(queue)
        [1, 2, 3, 4, 5, 6, 7, 8]
        """
        try:
            self._items.remove(self._value_to_item(value))
        except ValueError:
            raise KeyError(value)
        else:
            heapq.heapify(self._items)

    def discard(self, value: Value) -> None:
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
            self.remove(value)
        except KeyError:
            pass

    def peek(self) -> Value:
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

    def pop(self) -> Value:
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
