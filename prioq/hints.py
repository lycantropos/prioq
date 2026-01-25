from collections.abc import Callable
from typing import TypeAlias

from .core import hints as _hints

SortingKey: TypeAlias = Callable[[_hints.ValueT], _hints.KeyT]
