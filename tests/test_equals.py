from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.utils import (equivalence,
                         implication)


@given(strategies.priority_queues)
def test_reflexivity(priority_queue: PriorityQueue) -> None:
    assert priority_queue == priority_queue


@given(strategies.priority_queues, strategies.priority_queues)
def test_symmetry(first_priority_queue: PriorityQueue,
                  second_priority_queue: PriorityQueue) -> None:
    assert equivalence(first_priority_queue == second_priority_queue,
                       second_priority_queue == first_priority_queue)


@given(strategies.priority_queues, strategies.priority_queues,
       strategies.priority_queues)
def test_transitivity(first_priority_queue: PriorityQueue,
                      second_priority_queue: PriorityQueue,
                      third_priority_queue: PriorityQueue) -> None:
    assert implication(first_priority_queue == second_priority_queue
                       and second_priority_queue == third_priority_queue,
                       first_priority_queue == third_priority_queue)


@given(strategies.priority_queues, strategies.priority_queues)
def test_connection_with_inequality(first_priority_queue: PriorityQueue,
                                    second_priority_queue: PriorityQueue
                                    ) -> None:
    assert equivalence(not first_priority_queue == second_priority_queue,
                       first_priority_queue != second_priority_queue)
