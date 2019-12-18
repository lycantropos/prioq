from hypothesis import given

from prioq.base import PriorityQueue
from . import strategies


@given(strategies.priority_queues)
def test_basic(priority_queue: PriorityQueue) -> None:
    result = priority_queue.clear()

    assert result is None


@given(strategies.priority_queues)
def test_properties(priority_queue: PriorityQueue) -> None:
    priority_queue.clear()

    assert len(priority_queue) == 0
