import heapq
from abc import (ABC,
                 abstractmethod)
from collections import abc
from functools import partial
from operator import (attrgetter,
                      itemgetter)
from typing import (Iterator,
                    Optional,
                    Sequence,
                    Tuple)

from reprit.base import generate_repr

from .hints import (Domain,
                    Key,
                    Range)
from .utils import identity


class Reverser(ABC):
    @property
    @abstractmethod
    def value(self) -> Domain:
        pass

    @abstractmethod
    def __lt__(self, other: 'Reverser') -> bool:
        pass


class SimpleReverser(Reverser):
    __slots__ = ('_item',)

    def __init__(self, item: Domain) -> None:
        self._item = item

    __repr__ = generate_repr(__init__)

    @property
    def item(self) -> Domain:
        return self._item

    @property
    def value(self) -> Domain:
        return self._item

    def __lt__(self, other: 'SimpleReverser') -> bool:
        return (self._item > other._item
                if isinstance(other, SimpleReverser)
                else NotImplemented)

    def __eq__(self, other: 'SimpleReverser') -> bool:
        return (self._item == other._item
                if isinstance(other, SimpleReverser)
                else NotImplemented)


class ComplexReverser(Reverser):
    __slots__ = ('_item',)

    def __init__(self, item: Tuple[Range, Domain]) -> None:
        self._item = item

    __repr__ = generate_repr(__init__)

    @property
    def value(self) -> Domain:
        return self._item[1]

    @property
    def item(self) -> Domain:
        return self._item

    def __lt__(self, other: 'ComplexReverser') -> bool:
        return (self._item > other._item
                if isinstance(other, ComplexReverser)
                else NotImplemented)

    def __eq__(self, other: 'ComplexReverser') -> bool:
        return (self._item == other._item
                if isinstance(other, ComplexReverser)
                else NotImplemented)


def reverse_key(key: Optional[Key]) -> Key:
    return (SimpleReverser
            if key is None
            else partial(_to_complex_reverser, key))


def _to_complex_reverser(key: Key, value: Domain) -> ComplexReverser:
    return ComplexReverser(_to_item(key, value))


def _to_item(key: Key, value: Domain) -> Tuple[Range, Domain]:
    return key(value), value


class PriorityQueue(abc.MutableSet):
    """
    A priority queue is a mutable container
    that provides constant time lookup of the smallest (by default) element.

    Reference: https://en.wikipedia.org/wiki/Priority_queue
    """
    __slots__ = ('_key', '_reverse', '_items',
                 '_item_to_value', '_value_to_item')

    def __init__(self, *values: Domain,
                 key: Optional[Key] = None,
                 reverse: bool = False) -> None:
        """
        Initializes queue.

        :param values: initial values
        :param key: function of one argument to calculate priority.
        :param reverse: flag, if set to `True` specifies
        that values should be processed in descending order
        (from highest priority to lowest).
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
        self._items = [self._value_to_item(value) for value in values]
        heapq.heapify(self._items)

    __repr__ = generate_repr(__init__)

    @property
    def values(self) -> Sequence[Domain]:
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

        Complexity: O(n).
        """
        return value in self.values

    def __eq__(self, other: 'PriorityQueue') -> bool:
        """
        Checks if the queue is equal to the given one.

        Complexity: O(min(n, m)).
        """
        return (self._items == other._items
                if isinstance(other, PriorityQueue)
                else NotImplemented)

    def __len__(self) -> int:
        """
        Returns number of elements in the queue.

        Complexity: O(1).
        """
        return len(self._items)

    def __iter__(self) -> Iterator[Domain]:
        """
        Iterates over queue in sorted order.

        Complexity: O(n * log n).
        """
        return iter(sorted(self.values,
                           key=self._key,
                           reverse=self._reverse))

    def add(self, value: Domain) -> None:
        """
        Adds value to queue.

        Complexity: O(log n).
        """
        heapq.heappush(self._items, self._value_to_item(value))

    def discard(self, value: Domain) -> None:
        """
        Removes value from queue if present.

        Complexity: O(n).
        """
        try:
            self._items.remove(self._value_to_item(value))
        except ValueError:
            pass
        else:
            heapq.heapify(self._items)

    def peek(self) -> Domain:
        """
        Returns front value from the queue.

        Complexity: O(1).
        """
        try:
            return self._item_to_value(self._items[0])
        except IndexError:
            raise KeyError

    def pop(self) -> Domain:
        """
        Pops front value from the queue.

        Complexity: O(1).
        """
        try:
            return self._item_to_value(heapq.heappop(self._items))
        except IndexError:
            raise KeyError

    def clear(self) -> None:
        self._items.clear()
