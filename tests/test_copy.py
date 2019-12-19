import copy

from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies


@given(strategies.priority_queues)
def test_shallow(priority_queue: PriorityQueue) -> None:
    result = copy.copy(priority_queue)

    assert result is not priority_queue
    assert result == priority_queue
    assert result._items is priority_queue._items


@given(strategies.priority_queues)
def test_deep(priority_queue: PriorityQueue) -> None:
    result = copy.deepcopy(priority_queue)

    assert result is not priority_queue
    assert result == priority_queue
    assert result._items is not priority_queue._items
