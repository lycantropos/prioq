import pickle
from collections.abc import Iterable
from operator import is_
from typing import Any

from tests.hints import ValueT

equivalence = is_


def implication(antecedent: bool, consequent: bool, /) -> bool:
    return not antecedent or consequent


def capacity(iterable: Iterable[Any], /) -> int:
    return sum(1 for _ in iterable)


def identity(value: ValueT, /) -> ValueT:
    return value


def pickle_round_trip(object_: Any, /) -> Any:
    return pickle.loads(pickle.dumps(object_))
