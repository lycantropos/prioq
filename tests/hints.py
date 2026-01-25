from typing import TypeAlias, TypeVar

from prioq.base import PriorityQueue
from prioq.core.hints import Ordered
from prioq.hints import SortingKey

KeyT = TypeVar('KeyT', bound=Ordered)
ValueT = TypeVar('ValueT')
ValuesListWithKey: TypeAlias = tuple[
    list[ValueT], SortingKey[ValueT, KeyT] | None
]
PriorityQueuesPair: TypeAlias = tuple[
    PriorityQueue[KeyT, ValueT], PriorityQueue[KeyT, ValueT]
]
PriorityQueuesTriplet: TypeAlias = tuple[
    PriorityQueue[KeyT, ValueT],
    PriorityQueue[KeyT, ValueT],
    PriorityQueue[KeyT, ValueT],
]
