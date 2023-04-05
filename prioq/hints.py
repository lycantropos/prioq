import typing as _t

import typing_extensions as _te

from .core import hints as _hints

Key: _te.TypeAlias = _hints.Key
SortingKey = _t.Callable[[_hints.Value], _hints.Key]
Value: _te.TypeAlias = _hints.Value
