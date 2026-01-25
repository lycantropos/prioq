from copy import deepcopy

import pytest
from hypothesis import given

from prioq.base import PriorityQueue
from tests.hints import KeyT, ValueT
from tests.strategies import (
    empty_priority_queue_strategy,
    non_empty_priority_queues,
)


@given(empty_priority_queue_strategy)
def test_base_case(priority_queue: PriorityQueue[KeyT, ValueT]) -> None:
    with pytest.raises(IndexError):
        priority_queue.pop()


@given(non_empty_priority_queues)
def test_step(priority_queue: PriorityQueue[KeyT, ValueT]) -> None:
    original = deepcopy(priority_queue)

    result = priority_queue.pop()

    assert all(
        not item.key < priority_queue._sorting_key(result)
        for item in priority_queue._items
    )
    assert len(priority_queue) == len(original) - 1
