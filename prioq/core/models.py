from abc import (ABC,
                 abstractmethod)
from typing import Tuple

from reprit.base import generate_repr

from prioq.hints import (Key,
                         Value)


class Item(ABC):
    __slots__ = ()

    @abstractmethod
    def __lt__(self, other: 'Item') -> bool:
        """
        Checks if the object is lower than the other.
        """

    @property
    @abstractmethod
    def value(self) -> Value:
        """
        Returns associated value.
        """


class ComplexItem(Item):
    __slots__ = '_pair',

    def __init__(self, pair: Tuple[Key, Value]) -> None:
        self._pair = pair

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'ComplexItem') -> bool:
        return (self._pair == other._pair
                if isinstance(other, ComplexItem)
                else NotImplemented)

    def __lt__(self, other: 'ComplexItem') -> bool:
        return (self._pair[0] < other._pair[0]
                if isinstance(other, ComplexItem)
                else NotImplemented)

    @property
    def pair(self) -> Tuple[Key, Value]:
        return self._pair

    @property
    def value(self) -> Value:
        return self._pair[1]


class ComplexReversedItem(Item):
    __slots__ = '_pair',

    def __init__(self, pair: Tuple[Key, Value]) -> None:
        self._pair = pair

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'ComplexReversedItem') -> bool:
        return (self._pair == other._pair
                if isinstance(other, ComplexReversedItem)
                else NotImplemented)

    def __lt__(self, other: 'ComplexReversedItem') -> bool:
        return (self._pair[0] > other._pair[0]
                if isinstance(other, ComplexReversedItem)
                else NotImplemented)

    @property
    def pair(self) -> Tuple[Key, Value]:
        return self._pair

    @property
    def value(self) -> Value:
        return self._pair[1]


class SimpleItem(Item):
    __slots__ = '_value',

    def __init__(self, value: Value) -> None:
        self._value = value

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'SimpleItem') -> bool:
        return (self._value == other._value
                if isinstance(other, SimpleItem)
                else NotImplemented)

    def __lt__(self, other: 'SimpleItem') -> bool:
        return (self._value < other._value
                if isinstance(other, SimpleItem)
                else NotImplemented)

    @property
    def value(self) -> Value:
        return self._value


class SimpleReversedItem(Item):
    __slots__ = '_value',

    def __init__(self, value: Value) -> None:
        self._value = value

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'SimpleReversedItem') -> bool:
        return (self._value == other._value
                if isinstance(other, SimpleReversedItem)
                else NotImplemented)

    def __lt__(self, other: 'SimpleReversedItem') -> bool:
        return (self._value > other._value
                if isinstance(other, SimpleReversedItem)
                else NotImplemented)

    @property
    def value(self) -> Value:
        return self._value
