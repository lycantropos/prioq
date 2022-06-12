from typing import Callable as _Callable

from .core.hints import (Key,
                         Value)

SortingKey = _Callable[[Value], Key]
