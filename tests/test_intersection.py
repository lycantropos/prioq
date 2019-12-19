from hypothesis import given

from prioq.base import PriorityQueue
from tests.utils import (PriorityQueuesPair,
                         implication)
from . import strategies


@given(strategies.priority_queues_pairs)
def test_basic(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue & second_queue

    assert isinstance(result, PriorityQueue)


@given(strategies.priority_queues_pairs)
def test_properties(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue & second_queue

    assert len(result) <= min(len(first_queue), len(second_queue))
    assert all(value in first_queue for value in result)


@given(strategies.priority_queues)
def test_idempotence(priority_queue: PriorityQueue) -> None:
    result = priority_queue & priority_queue

    assert result == priority_queue


@given(strategies.priority_queues_pairs)
def test_left_absorbing_element(priority_queues_pair: PriorityQueuesPair
                                ) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue & second_queue

    assert implication(not first_queue, not result)


@given(strategies.priority_queues_pairs)
def test_right_absorbing_element(priority_queues_pair: PriorityQueuesPair
                                 ) -> None:
    first_queue, second_queue = priority_queues_pair

    result = second_queue & first_queue

    assert implication(not first_queue, not result)


@given(strategies.priority_queues_pairs)
def test_absorption_identity(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue & (first_queue | second_queue)

    assert result == first_queue


@given(strategies.priority_queues_pairs)
def test_connection_with_subset_relation(
        priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue & second_queue

    assert result <= first_queue
