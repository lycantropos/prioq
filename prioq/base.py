from functools import partial as _partial
from heapq import (heapify as _heapify,
                   heappop as _heappop,
                   heappush as _heappush)
from typing import (Any as _Any,
                    Generic as _Generic,
                    List as _List,
                    Optional as _Optional,
                    cast, overload as _overload)

from reprit.base import generate_repr as _generate_repr

from .core.hints import Value as _Value
from .core.order import (NaturalOrder as _NaturalOrder,
                         ReversedOrder as _ReversedOrder)
from .hints import SortingKey as _SortingKey


class PriorityQueue(_Generic[_Value]):
    """
    A priority queue is a mutable container
    that provides constant time lookup of the smallest (by default) element.

    Reference: https://en.wikipedia.org/wiki/Priority_queue
    """
    __slots__ = '_sorting_key', '_items', '_key', '_reverse'

    def __init__(self,
                 *values: _Value,
                 key: _Optional[_SortingKey] = None,
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
        self._sorting_key: _SortingKey = cast(
                _SortingKey,
                (_ReversedOrder if reverse else _NaturalOrder)
                if key is None
                else (_partial(_to_reversed_key, key) if reverse else key)
        )
        self._items = [(self._sorting_key(value), value) for value in values]
        _heapify(self._items)
        self._key = key
        self._reverse = reverse

    __repr__ = _generate_repr(__init__)

    @_overload
    def __eq__(self, other: 'PriorityQueue[_Value]') -> bool:
        ...

    @_overload
    def __eq__(self, other: _Any) -> _Any:
        ...

    def __eq__(self, other):

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
    def key(self) -> _Optional[_SortingKey]:
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

    def peek(self) -> _Value:
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
            _, value = self._items[0]
        except IndexError:
            raise ValueError('Priority queue is empty') from None
        else:
            return value

    def pop(self) -> _Value:
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
        _, value = _heappop(self._items)
        return value

    def push(self, value: _Value) -> None:
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
        _heappush(self._items, (self._sorting_key(value), value))

    def remove(self, value: _Value) -> None:
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
            self._items.remove((self._sorting_key(value), value))
        except ValueError:
            raise ValueError('{!r} is not in priority queue'
                             .format(value)) from None
        else:
            _heapify(self._items)

    def values(self) -> _List[_Value]:
        """
        Returns elements of the queue.

        Complexity: O(len(self) * log len(self)).

        >>> queue = PriorityQueue(*range(5))
        >>> queue.values()
        [0, 1, 2, 3, 4]
        """
        return [value for _, value in sorted(self._items)]


def _to_reversed_key(key: _SortingKey, value: _Value) -> _ReversedOrder:
    return _ReversedOrder(key(value))
