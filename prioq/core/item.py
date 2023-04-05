from __future__ import annotations

import typing as _t

import typing_extensions as _te
from reprit.base import generate_repr as _generate_repr

from .hints import (Key,
                    Value)


class Item(_t.Generic[Key, Value]):
    key: Key
    value: Value

    __slots__ = 'key', 'value'

    def __init__(self, key: Key, value: Value) -> None:
        self.key, self.value = key, value

    @_t.overload
    def __lt__(self, other: _te.Self) -> bool:
        ...

    @_t.overload
    def __lt__(self, other: _t.Any) -> _t.Any:
        ...

    def __lt__(self, other: _t.Any) -> _t.Any:
        return (self.key < other.key
                if isinstance(other, Item)
                else NotImplemented)

    __repr__ = _generate_repr(__init__)
