import typing as _t

import typing_extensions as _te
from reprit.base import generate_repr

from .hints import Ordered

_T = _t.TypeVar('_T',
                bound=Ordered)


class NaturalOrder(_t.Generic[_T]):
    __slots__ = '_value',

    def __init__(self, _value: _T) -> None:
        self._value = _value

    __repr__ = generate_repr(__init__)

    @_t.overload
    def __eq__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __eq__(self, other: _t.Any) -> _t.Any:
        ...

    def __eq__(self, other: _t.Any) -> _t.Any:
        return (self._value == other._value
                if isinstance(other, NaturalOrder)
                else NotImplemented)

    @_t.overload
    def __lt__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __lt__(self, other: _t.Any) -> _t.Any:
        ...

    def __lt__(self, other: _t.Any) -> _t.Any:
        return (self._value < other._value
                if isinstance(other, NaturalOrder)
                else NotImplemented)


class ReversedOrder(_t.Generic[_T]):
    __slots__ = '_value',

    def __init__(self, _value: _T) -> None:
        self._value = _value

    __repr__ = generate_repr(__init__)

    @_t.overload
    def __eq__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __eq__(self, other: _t.Any) -> _t.Any:
        ...

    def __eq__(self, other: _t.Any) -> _t.Any:
        return (self._value == other._value
                if isinstance(other, ReversedOrder)
                else NotImplemented)

    @_t.overload
    def __lt__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __lt__(self, other: _t.Any) -> _t.Any:
        ...

    def __lt__(self, other: _t.Any) -> _t.Any:
        return (other._value < self._value
                if isinstance(other, ReversedOrder)
                else NotImplemented)
