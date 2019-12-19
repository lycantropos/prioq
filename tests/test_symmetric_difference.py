from hypothesis import given

from prioq.base import PriorityQueue
from tests.utils import (PriorityQueuesPair,
                         implication)
from . import strategies


@given(strategies.priority_queues_pairs)
def test_basic(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue ^ second_queue

    assert isinstance(result, PriorityQueue)


@given(strategies.priority_queues_pairs)
def test_properties(priority_queues_pair: PriorityQueuesPair) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue ^ second_queue

    assert len(result) <= len(first_queue) + len(second_queue)


@given(strategies.priority_queues)
def test_self_inverse(priority_queue: PriorityQueue) -> None:
    result = priority_queue ^ priority_queue

    assert not result


@given(strategies.priority_queues_pairs)
def test_left_neutral_element(priority_queues_pair: PriorityQueuesPair
                              ) -> None:
    first_queue, second_queue = priority_queues_pair

    result = first_queue ^ second_queue

    assert implication(not first_queue, result == second_queue)


@given(strategies.priority_queues_pairs)
def test_right_neutral_element(priority_queues_pair: PriorityQueuesPair
                               ) -> None:
    first_queue, second_queue = priority_queues_pair

    result = second_queue ^ first_queue

    assert implication(not first_queue, result == second_queue)
