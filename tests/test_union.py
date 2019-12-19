from hypothesis import given

from prioq.base import PriorityQueue
from tests.utils import (PriorityQueuesPair,
                         PriorityQueuesTriplet,
                         implication)
from . import strategies


@given(strategies.priority_queues_pairs)
def test_basic(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue | second_queue

    assert isinstance(result, PriorityQueue)


@given(strategies.priority_queues_pairs)
def test_properties(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue | second_queue

    assert len(result) <= len(first_queue) + len(second_queue)
    assert (all(value in result
                for value in first_queue)
            and all(value in result
                    for value in second_queue))
    assert ((not first_queue or not result.isdisjoint(first_queue))
            and (not second_queue or not result.isdisjoint(second_queue)))


@given(strategies.priority_queues_triplets)
def test_associativity(priority_queues_triplet: PriorityQueuesTriplet) -> None:
    first_queue, mid_priority_queue, second_queue = priority_queues_triplet

    result = (first_queue | mid_priority_queue) | second_queue

    assert result == first_queue | (mid_priority_queue | second_queue)


@given(strategies.priority_queues_pairs)
def test_connection_with_subset_relation(
        priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue | second_queue

    assert first_queue <= result


@given(strategies.priority_queues_pairs)
def test_connection_with_disjoint(
        priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue | second_queue

    assert implication(first_queue.isdisjoint(second_queue),
                       len(result) == len(first_queue) + len(second_queue))
