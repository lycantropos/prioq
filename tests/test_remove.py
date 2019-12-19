from copy import deepcopy
from typing import Tuple

import pytest
from hypothesis import given

from prioq.base import PriorityQueue
from prioq.hints import Domain
from tests import strategies


@given(strategies.empty_priority_queues_with_values)
def test_base_case(
        priority_queue_with_value: Tuple[PriorityQueue, Domain]) -> None:
    priority_queue, value = priority_queue_with_value

    with pytest.raises(KeyError):
        priority_queue.remove(value)


@given(strategies.non_empty_priority_queues_with_their_values)
def test_step(priority_queue_with_value: Tuple[PriorityQueue, Domain]) -> None:
    priority_queue, value = priority_queue_with_value
    original = deepcopy(priority_queue)

    priority_queue.remove(value)

    assert len(priority_queue) == len(original) - 1
