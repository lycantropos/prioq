from hypothesis import given

from prioq.base import PriorityQueue
from tests.hints import KeyT, ValueT
from tests.strategies import priority_queue_strategy


@given(priority_queue_strategy)
def test_basic(priority_queue: PriorityQueue[KeyT, ValueT]) -> None:
    result = priority_queue.clear()  # type: ignore[func-returns-value]

    assert result is None


@given(priority_queue_strategy)
def test_properties(priority_queue: PriorityQueue[KeyT, ValueT]) -> None:
    priority_queue.clear()

    assert len(priority_queue) == 0
