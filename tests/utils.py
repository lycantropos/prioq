import pickle
from typing import (Any,
                    Iterable,
                    List,
                    Optional,
                    Tuple)

from hypothesis.strategies import SearchStrategy

from prioq.base import PriorityQueue
from prioq.hints import (Domain,
                         Key)

Strategy = SearchStrategy
ValuesListWithKey = Tuple[List[Domain], Optional[Key]]
ValuesListsPairWithKey = Tuple[List[Domain], List[Domain], Optional[Key]]
ValuesListsTripletWithKey = Tuple[List[Domain], List[Domain], List[Domain],
                                  Optional[Key]]
PriorityQueuesPair = Tuple[PriorityQueue, PriorityQueue]
PriorityQueuesTriplet = Tuple[PriorityQueue, PriorityQueue, PriorityQueue]


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def capacity(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)


def pickle_round_trip(object_: Domain) -> Domain:
    return pickle.loads(pickle.dumps(object_))
