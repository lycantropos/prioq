from hypothesis import given

from prioq.base import PriorityQueue
from . import strategies


@given(strategies.priority_queues)
def test_properties(priority_queue: PriorityQueue) -> None:
    priority_queue.clear()

    assert len(priority_queue) == 0
