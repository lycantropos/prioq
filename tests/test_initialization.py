from collections.abc import Callable

from hypothesis import given

from prioq.base import PriorityQueue
from tests import strategies
from tests.hints import KeyT, ValueT


@given(strategies.values_list_with_key_strategy, strategies.booleans)
def test_basic(
    values_with_key: tuple[list[ValueT], Callable[[ValueT], KeyT] | None],
    reverse: bool,
) -> None:
    values, key = values_with_key

    result = PriorityQueue(*values, key=key, reverse=reverse)

    assert len(result) == len(values)
    assert all(value in result.values() for value in values)
    assert result.key is key
    assert result.reverse is reverse
