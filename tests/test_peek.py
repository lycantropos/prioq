import pytest
from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies


@given(strategies.empty_priority_queues)
def test_base_case(priority_queue: PriorityQueue) -> None:
    with pytest.raises(ValueError):
        priority_queue.peek()


@given(strategies.non_empty_priority_queues)
def test_step(priority_queue: PriorityQueue) -> None:
    result = priority_queue.peek()

    assert result in priority_queue.values()
    assert all(not item.key < priority_queue._sorting_key(result)
               for item in priority_queue._items)
