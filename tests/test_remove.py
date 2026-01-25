from copy import deepcopy

import pytest
from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.hints import KeyT, ValueT


@given(strategies.empty_priority_queue_with_value_strategy)
def test_base_case(
    priority_queue_with_value: tuple[PriorityQueue[KeyT, ValueT], ValueT],
) -> None:
    priority_queue, value = priority_queue_with_value

    with pytest.raises(ValueError):
        priority_queue.remove(value)


@given(strategies.non_empty_priority_queues_with_their_values)
def test_step(
    priority_queue_with_value: tuple[PriorityQueue[KeyT, ValueT], ValueT],
) -> None:
    priority_queue, value = priority_queue_with_value
    original = deepcopy(priority_queue)

    priority_queue.remove(value)

    assert len(priority_queue) == len(original) - 1
