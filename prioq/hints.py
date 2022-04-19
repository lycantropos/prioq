from typing import Callable as _Callable

from .core import hints as _hints

Key = _hints.Key
Value = _hints.Value
SortingKey = _Callable[[Value], Key]
