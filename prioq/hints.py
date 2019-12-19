from typing import (Callable,
                    TypeVar)

Value = TypeVar('Value')
Key = TypeVar('Key')
SortingKey = Callable[[Value], Key]
