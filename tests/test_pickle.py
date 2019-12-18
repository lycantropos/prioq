from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.utils import pickle_round_trip


@given(strategies.priority_queues)
def test_round_trip(priority_queue: PriorityQueue) -> None:
    assert pickle_round_trip(priority_queue) == priority_queue
