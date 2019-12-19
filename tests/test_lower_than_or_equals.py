from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.utils import (PriorityQueuesPair,
                         PriorityQueuesTriplet,
                         equivalence,
                         implication)


@given(strategies.priority_queues)
def test_reflexivity(priority_queue: PriorityQueue) -> None:
    assert priority_queue <= priority_queue


@given(strategies.priority_queues_pairs)
def test_antisymmetry(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    assert equivalence(first_queue <= second_queue <= first_queue,
                       first_queue == second_queue)


@given(strategies.priority_queues_triplets)
def test_transitivity(priority_queues_triplet: PriorityQueuesTriplet) -> None:
    first_queue, second_queue, third_queue = priority_queues_triplet

    assert implication(first_queue <= second_queue <= third_queue,
                       first_queue <= third_queue)


@given(strategies.priority_queues_pairs)
def test_connection_with_lower_than(priority_queues_pair: PriorityQueuesPair
                                    ) -> None:
    first_queue, second_queue = priority_queues_pair

    assert implication(first_queue < second_queue, first_queue <= second_queue)


@given(strategies.priority_queues_pairs)
def test_connection_with_greater_than_or_equals(
        priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    assert equivalence(first_queue <= second_queue,
                       second_queue >= first_queue)
