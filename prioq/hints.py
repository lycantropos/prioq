from typing import (Callable,
                    TypeVar)

Domain = TypeVar('Domain')
OtherDomain = TypeVar('OtherDomain')
Range = TypeVar('Range')
Key = Callable[[Domain], Range]
