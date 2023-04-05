import typing as _t

import typing_extensions as _te


class Ordered(_te.Protocol):
    def __lt__(self, other: _te.Self) -> bool:
        ...


Value = _t.TypeVar('Value')
Key = _t.TypeVar('Key',
                 bound=Ordered)
