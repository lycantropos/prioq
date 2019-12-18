from typing import Tuple

from hypothesis import given

from prioq.base import PriorityQueue
from prioq.hints import Domain
from . import strategies


@given(strategies.priority_queues_with_values)
def test_properties(priority_queue_with_value: Tuple[PriorityQueue, Domain]
                    ) -> None:
    priority_queue, value = priority_queue_with_value

    priority_queue.add(value)

    assert value in priority_queue
    assert len(priority_queue) > 0
