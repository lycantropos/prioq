from typing import (Any,
                    Iterable)

from hypothesis.strategies import SearchStrategy

Strategy = SearchStrategy


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def capacity(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)
