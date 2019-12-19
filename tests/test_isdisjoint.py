from typing import Tuple

from hypothesis import given

from prioq.base import PriorityQueue
from tests.utils import (PriorityQueuesPair,
                         equivalence,
                         implication)
from . import strategies


@given(strategies.priority_queues_pairs)
def test_basic(priority_queues_pair: PriorityQueuesPair) -> None:
    first_priority_queue, second_priority_queue = priority_queues_pair

    result = first_priority_queue.isdisjoint(second_priority_queue)

    assert isinstance(result, bool)


@given(strategies.priority_queues_pairs)
def test_empty(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    assert implication(not first_queue, first_queue.isdisjoint(second_queue))


@given(strategies.priority_queues_pairs)
def test_connection_with_lower_than_or_equal(
        priority_queues_pair: PriorityQueuesPair) -> None:
    left_queue, right_queue = priority_queues_pair

    assert implication(left_queue and right_queue
                       and left_queue <= right_queue,
                       not left_queue.isdisjoint(right_queue))


@given(strategies.priority_queues_pairs)
def test_symmetry(priority_queues_pair: PriorityQueuesPair) -> None:
    first_priority_queue, second_priority_queue = priority_queues_pair

    assert equivalence(first_priority_queue.isdisjoint(second_priority_queue),
                       second_priority_queue.isdisjoint(first_priority_queue))
