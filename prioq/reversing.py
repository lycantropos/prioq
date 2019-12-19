from abc import (ABC,
                 abstractmethod)
from typing import Tuple

from reprit.base import generate_repr

from prioq.hints import (Key,
                         Value)


class Reverser(ABC):
    @property
    @abstractmethod
    def item(self) -> Value:
        """
        Returns underlying item.
        """

    @property
    @abstractmethod
    def value(self) -> Value:
        """
        Returns associated value.
        """

    @abstractmethod
    def __lt__(self, other: 'Reverser') -> bool:
        """
        Checks if the object is greater than the other.
        """


class SimpleReverser(Reverser):
    __slots__ = ('_item',)

    def __init__(self, item: Value) -> None:
        self._item = item

    __repr__ = generate_repr(__init__)

    @property
    def item(self) -> Value:
        """
        >>> reverser = SimpleReverser(0)
        >>> reverser.item
        0
        """
        return self._item

    @property
    def value(self) -> Value:
        """
        >>> reverser = SimpleReverser(0)
        >>> reverser.value
        0
        """
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

    def __init__(self, item: Tuple[Key, Value]) -> None:
        self._item = item

    __repr__ = generate_repr(__init__)

    @property
    def value(self) -> Value:
        """
        >>> reverser = ComplexReverser((0, 1))
        >>> reverser.value
        1
        """
        return self._item[1]

    @property
    def item(self) -> Value:
        """
        >>> reverser = ComplexReverser((0, 1))
        >>> reverser.item
        (0, 1)
        """
        return self._item

    def __lt__(self, other: 'ComplexReverser') -> bool:
        return (self._item > other._item
                if isinstance(other, ComplexReverser)
                else NotImplemented)

    def __eq__(self, other: 'ComplexReverser') -> bool:
        return (self._item == other._item
                if isinstance(other, ComplexReverser)
                else NotImplemented)
