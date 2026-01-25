from typing import TypeVar

from typing_extensions import Protocol, Self


class Ordered(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...


class HasCustomRepr(Protocol):
    def __repr__(self, /) -> str:
        raise NotImplementedError


ValueT = TypeVar('ValueT')
KeyT = TypeVar('KeyT', bound=Ordered)
