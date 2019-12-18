from copy import deepcopy

import pytest
from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies


@given(strategies.empty_priority_queues)
def test_base_case(priority_queue: PriorityQueue) -> None:
    with pytest.raises(KeyError):
        priority_queue.pop()


@given(strategies.non_empty_priority_queues)
def test_step(priority_queue: PriorityQueue) -> None:
    original = deepcopy(priority_queue)

    result = priority_queue.pop()

    assert all(not item < priority_queue._value_to_item(result)
               for item in priority_queue._items)
    assert len(priority_queue) == len(original) - 1
