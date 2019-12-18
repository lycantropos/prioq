from typing import (Callable,
                    TypeVar)

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Key = Callable[[Domain], Range]
