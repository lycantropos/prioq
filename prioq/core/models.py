from abc import (ABC,
                 abstractmethod)

from reprit.base import generate_repr

from .hints import (Key,
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
    __slots__ = '_key', '_value'

    def __init__(self, key: Key, value: Value) -> None:
        self._key, self._value = key, value

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'ComplexItem') -> bool:
        return (self.key == other.key and self.value == other.value
                if isinstance(other, ComplexItem)
                else NotImplemented)

    def __lt__(self, other: 'ComplexItem') -> bool:
        return (self.key < other.key
                if isinstance(other, ComplexItem)
                else NotImplemented)

    @property
    def key(self) -> Key:
        return self._key

    @property
    def value(self) -> Value:
        return self._value


class ComplexReversedItem(Item):
    __slots__ = '_key', '_value'

    def __init__(self, key: Key, value: Value) -> None:
        self._key, self._value = key, value

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'ComplexReversedItem') -> bool:
        return (self.key == other.key and self.value == other.value
                if isinstance(other, ComplexReversedItem)
                else NotImplemented)

    def __lt__(self, other: 'ComplexReversedItem') -> bool:
        return (self.key > other.key
                if isinstance(other, ComplexReversedItem)
                else NotImplemented)

    @property
    def key(self) -> Key:
        return self._key

    @property
    def value(self) -> Value:
        return self._value


class SimpleItem(Item):
    __slots__ = '_value',

    def __init__(self, value: Value) -> None:
        self._value = value

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: 'SimpleItem') -> bool:
        return (self.value == other.value
                if isinstance(other, SimpleItem)
                else NotImplemented)

    def __lt__(self, other: 'SimpleItem') -> bool:
        return (self.value < other.value
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
        return (self.value == other.value
                if isinstance(other, SimpleReversedItem)
                else NotImplemented)

    def __lt__(self, other: 'SimpleReversedItem') -> bool:
        return (self.value > other.value
                if isinstance(other, SimpleReversedItem)
                else NotImplemented)

    @property
    def value(self) -> Value:
        return self._value
