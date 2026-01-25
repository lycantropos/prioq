from hypothesis import given

from prioq.base import PriorityQueue
from tests.hints import KeyT, ValueT
from tests.strategies import priority_queue_strategy
from tests.utils import pickle_round_trip


@given(priority_queue_strategy)
def test_round_trip(priority_queue: PriorityQueue[KeyT, ValueT]) -> None:
    assert pickle_round_trip(priority_queue) == priority_queue
