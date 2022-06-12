from typing import (Any,
                    Generic,
                    TypeVar)

from reprit.base import generate_repr

from .hints import Ordered

_T = TypeVar('_T',
             bound=Ordered)


class NaturalOrder(Generic[_T]):
    __slots__ = '_value',

    def __init__(self, _value: _T) -> None:
        self._value = _value

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: Any) -> Any:
        return (self._value == other._value
                if isinstance(other, NaturalOrder)
                else NotImplemented)

    def __lt__(self, other: Any) -> Any:
        return (self._value < other._value
                if isinstance(other, NaturalOrder)
                else NotImplemented)


class ReversedOrder(Generic[_T]):
    __slots__ = '_value',

    def __init__(self, _value: _T) -> None:
        self._value = _value

    __repr__ = generate_repr(__init__)

    def __eq__(self, other: Any) -> Any:
        return (self._value == other._value
                if isinstance(other, ReversedOrder)
                else NotImplemented)

    def __lt__(self, other: Any) -> Any:
        return (other._value < self._value
                if isinstance(other, ReversedOrder)
                else NotImplemented)
