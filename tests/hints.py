from collections.abc import Callable
from typing import TypeAlias, TypeVar

from prioq.base import PriorityQueue
from prioq.hints import Ordered

KeyT = TypeVar('KeyT', bound=Ordered)
ValueT = TypeVar('ValueT')
ValuesListWithKey: TypeAlias = tuple[
    list[ValueT], Callable[[ValueT], KeyT] | None
]
PriorityQueuesPair: TypeAlias = tuple[
    PriorityQueue[KeyT, ValueT], PriorityQueue[KeyT, ValueT]
]
PriorityQueuesTriplet: TypeAlias = tuple[
    PriorityQueue[KeyT, ValueT],
    PriorityQueue[KeyT, ValueT],
    PriorityQueue[KeyT, ValueT],
]
