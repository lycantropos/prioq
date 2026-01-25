from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.hints import KeyT, ValueT


@given(strategies.priority_queues_with_values)
def test_basic(
    priority_queue_with_value: tuple[PriorityQueue[KeyT, ValueT], ValueT],
) -> None:
    priority_queue, value = priority_queue_with_value

    result = priority_queue.push(value)  # type: ignore[func-returns-value]

    assert result is None


@given(strategies.priority_queues_with_values)
def test_properties(
    priority_queue_with_value: tuple[PriorityQueue[KeyT, ValueT], ValueT],
) -> None:
    priority_queue, value = priority_queue_with_value

    priority_queue.push(value)

    assert value in priority_queue.values()
    assert len(priority_queue) > 0
