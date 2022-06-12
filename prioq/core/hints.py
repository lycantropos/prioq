from typing import TypeVar

from typing_extensions import Protocol

_T = TypeVar('_T',
             contravariant=True)


class Ordered(Protocol[_T]):
    def __lt__(self: _T, other: _T) -> bool:
        ...


Value = TypeVar('Value')
Key = TypeVar('Key', bound=Ordered)
