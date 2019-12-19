from operator import (gt,
                      lt)
from typing import (Iterable,
                    Optional)

from .hints import (SortingKey,
                    Value)


def identity(value: Value) -> Value:
    return value


def intersect_sorted(left: Iterable[Value], right: Iterable[Value],
                     *,
                     key: Optional[SortingKey],
                     reverse: bool) -> Iterable[Value]:
    """
    Returns intersection of sorted iterables.

    Complexity: O(min(len(left), len(right))).
    """
    operator = gt if reverse else lt
    if key is None:
        left, right = iter(left), iter(right)
        try:
            left_value, right_value = next(left), next(right)
        except StopIteration:
            return
        while True:
            if operator(left_value, right_value):
                try:
                    left_value = next(left)
                except StopIteration:
                    return
            elif operator(right_value, left_value):
                try:
                    right_value = next(right)
                except StopIteration:
                    return
            else:
                # equal
                yield left_value
                try:
                    left_value, right_value = next(left), next(right)
                except StopIteration:
                    return
    else:
        left, right = (((key(element), element) for element in left),
                       (key(element) for element in right))
        try:
            (left_key, left_value), right_key = next(left), next(right)
        except StopIteration:
            return
        while True:
            if operator(left_key, right_key):
                try:
                    left_key, left_value = next(left)
                except StopIteration:
                    return
            elif operator(right_key, left_key):
                try:
                    right_key = next(right)
                except StopIteration:
                    return
            else:
                # equal
                yield left_value
                try:
                    (left_key, left_value), right_key = next(left), next(right)
                except StopIteration:
                    return


def subtract_sorted(left: Iterable[Value], right: Iterable[Value],
                    *,
                    key: Optional[SortingKey],
                    reverse: bool) -> Iterable[Value]:
    """
    Returns subtraction of sorted iterables.

    Complexity: O(min(len(left), len(right))).
    """
    operator = gt if reverse else lt
    if key is None:
        left, right = iter(left), iter(right)
        try:
            left_value = next(left)
        except StopIteration:
            return
        try:
            right_value = next(right)
        except StopIteration:
            yield left_value
            yield from left
            return
        while True:
            if operator(left_value, right_value):
                yield left_value
                try:
                    left_value = next(left)
                except StopIteration:
                    return
            elif operator(right_value, left_value):
                try:
                    right_value = next(right)
                except StopIteration:
                    yield left_value
                    yield from left
                    return
            else:
                # equal
                try:
                    left_value = next(left)
                except StopIteration:
                    return
                try:
                    right_value = next(right)
                except StopIteration:
                    yield left_value
                    yield from left
                    return
    else:
        left, right = (((key(element), element) for element in left),
                       (key(element) for element in right))
        try:
            left_key, left_value = next(left)
        except StopIteration:
            return
        try:
            right_key = next(right)
        except StopIteration:
            yield left_value
            yield from (value for _, value in left)
            return
        while True:
            if operator(left_key, right_key):
                yield left_value
                try:
                    left_key, left_value = next(left)
                except StopIteration:
                    return
            elif operator(right_key, left_key):
                try:
                    right_key = next(right)
                except StopIteration:
                    yield left_value
                    yield from (value for _, value in left)
                    return
            else:
                # equal
                try:
                    left_key, left_value = next(left)
                except StopIteration:
                    return
                try:
                    right_key = next(right)
                except StopIteration:
                    yield left_value
                    yield from (value for _, value in left)
                    return
