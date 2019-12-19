from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.utils import capacity


@given(strategies.priority_queues)
def test_size(priority_queue: PriorityQueue) -> None:
    result = iter(priority_queue)

    assert capacity(result) == len(priority_queue)


@given(strategies.priority_queues)
def test_elements(priority_queue: PriorityQueue) -> None:
    result = iter(priority_queue)

    assert all(element in priority_queue for element in result)


@given(strategies.priority_queues)
def test_order(priority_queue: PriorityQueue) -> None:
    result = iter(priority_queue)

    assert list(result) == sorted(priority_queue._values,
                                  key=priority_queue.key,
                                  reverse=priority_queue.reverse)
