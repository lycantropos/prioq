import copy

from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.hints import KeyT, ValueT


@given(strategies.priority_queue_strategy)
def test_shallow(priority_queue: PriorityQueue[KeyT, ValueT]) -> None:
    result = copy.copy(priority_queue)

    assert result is not priority_queue
    assert result == priority_queue


@given(strategies.priority_queue_strategy)
def test_deep(priority_queue: PriorityQueue[KeyT, ValueT]) -> None:
    result = copy.deepcopy(priority_queue)

    assert result is not priority_queue
    assert result == priority_queue
