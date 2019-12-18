from typing import (List,
                    Optional,
                    Tuple)

from hypothesis import given

from prioq.base import PriorityQueue
from prioq.hints import (Domain,
                         Key)
from tests import strategies


@given(strategies.values_lists_with_keys, strategies.booleans)
def test_basic(values_with_key: Tuple[List[Domain], Optional[Key]],
               reverse: bool) -> None:
    values, key = values_with_key

    result = PriorityQueue(*values,
                           key=key,
                           reverse=reverse)

    assert len(result.values) == len(values)
    assert all(value in result.values for value in values)
    assert result.key is key
    assert result.reverse is reverse
