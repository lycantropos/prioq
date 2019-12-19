from typing import Tuple

from hypothesis import given

from prioq.base import PriorityQueue
from prioq.hints import Value
from tests import strategies


@given(strategies.priority_queues_with_values)
def test_basic(priority_queue_with_value: Tuple[PriorityQueue, Value]
               ) -> None:
    priority_queue, value = priority_queue_with_value

    result = priority_queue.add(value)

    assert result is None


@given(strategies.priority_queues_with_values)
def test_properties(priority_queue_with_value: Tuple[PriorityQueue, Value]
                    ) -> None:
    priority_queue, value = priority_queue_with_value

    priority_queue.add(value)

    assert value in priority_queue
    assert len(priority_queue) > 0
