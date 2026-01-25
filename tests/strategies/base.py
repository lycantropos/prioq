import math
from collections.abc import Callable
from functools import partial
from operator import not_
from typing import Any

from hypothesis import strategies as _st

from prioq.base import PriorityQueue
from tests.hints import KeyT, PriorityQueuesPair, PriorityQueuesTriplet, ValueT
from tests.utils import identity

from .factories import (
    to_priority_queue,
    to_priority_queue_with_their_value_strategy,
    to_priority_queue_with_value,
    to_value_sequence_with_key_strategy,
    to_value_sequences_with_key_strategy,
    to_value_with_key_strategy,
    to_values_tuples_with_keys,
)

booleans = _st.booleans()
maybe_infinite_numbers_keys = _st.sampled_from([identity, abs])
finite_number_sorting_keys = maybe_infinite_numbers_keys | _st.sampled_from(
    [round, math.trunc, math.ceil, math.floor]
)
strings_keys = _st.sampled_from(
    [
        identity,
        str.lower,
        str.upper,
        str.title,
        str.capitalize,
        str.casefold,
        str.swapcase,
    ]
)

ordered_value_strategy_sorting_keys = {
    _st.integers(): finite_number_sorting_keys,
    _st.floats(allow_nan=False): maybe_infinite_numbers_keys,
    _st.floats(
        allow_nan=False, allow_infinity=False
    ): finite_number_sorting_keys,
    _st.booleans(): _st.just(not_) | finite_number_sorting_keys,
    _st.text(): strings_keys,
}
unordered_values = _st.sampled_from([None, Ellipsis, NotImplemented])


def to_zero(_: Any, /) -> int:
    return 0


values_keys = {
    **ordered_value_strategy_sorting_keys,
    unordered_values: _st.sampled_from([id, to_zero]),
}
base_values_with_keys_strategies = _st.sampled_from(list(values_keys.items()))
value_with_key_strategy_strategy = _st.sampled_from(
    [
        (sortables, _st.none())
        for sortables in ordered_value_strategy_sorting_keys
    ]
) | _st.recursive(
    base_values_with_keys_strategies, to_values_tuples_with_keys, max_leaves=10
)
value_with_key_strategy = (
    _st.sampled_from(list(ordered_value_strategy_sorting_keys.keys())).flatmap(
        lambda values: _st.tuples(values, _st.none())
    )
) | value_with_key_strategy_strategy.flatmap(to_value_with_key_strategy)
value_list_with_key_strategy = value_with_key_strategy_strategy.flatmap(
    to_value_sequence_with_key_strategy
)
empty_value_list_with_key_strategy = value_with_key_strategy_strategy.flatmap(
    partial(to_value_sequence_with_key_strategy, max_size=0)
)
non_empty_value_list_with_key_strategy = (
    value_with_key_strategy_strategy.flatmap(
        partial(to_value_sequence_with_key_strategy, min_size=1)
    )
)
single_value_with_key_strategy = value_with_key_strategy_strategy.flatmap(
    partial(to_value_sequence_with_key_strategy, min_size=1, max_size=1)
)
priority_queue_strategy = _st.builds(
    to_priority_queue, value_list_with_key_strategy, booleans
)
empty_priority_queue_strategy = _st.builds(
    to_priority_queue, empty_value_list_with_key_strategy, booleans
)
non_empty_priority_queues = _st.builds(
    to_priority_queue, non_empty_value_list_with_key_strategy, booleans
)
priority_queues_with_values = _st.builds(
    to_priority_queue_with_value,
    non_empty_value_list_with_key_strategy,
    booleans,
)
empty_priority_queue_with_value_strategy = _st.builds(
    to_priority_queue_with_value, single_value_with_key_strategy, booleans
)
non_empty_priority_queues_with_their_values = (
    non_empty_priority_queues.flatmap(
        to_priority_queue_with_their_value_strategy
    )
)


def to_priority_queues_pair(
    values_lists_pair_with_key: tuple[
        tuple[list[ValueT], list[ValueT]], Callable[[ValueT], KeyT] | None
    ],
    first_reverse: bool,
    second_reverse: bool,
) -> PriorityQueuesPair[KeyT, ValueT]:
    (first_values_list, second_values_list), key = values_lists_pair_with_key
    first_priority_queue = PriorityQueue(
        *first_values_list, key=key, reverse=first_reverse
    )
    second_priority_queue = PriorityQueue(
        *second_values_list, key=key, reverse=second_reverse
    )
    return first_priority_queue, second_priority_queue


priority_queues_pairs = _st.builds(
    to_priority_queues_pair,
    value_with_key_strategy_strategy.flatmap(
        partial(to_value_sequences_with_key_strategy, sizes=[(0, None)] * 2)
    ),
    booleans,
    booleans,
)


def to_priority_queues_triplet(
    values_lists_triplet_with_key: tuple[
        tuple[list[ValueT], list[ValueT], list[ValueT]],
        Callable[[ValueT], KeyT] | None,
    ],
    first_reverse: bool,
    second_reverse: bool,
    third_reverse: bool,
) -> PriorityQueuesTriplet[KeyT, ValueT]:
    (first_values_list, second_values_list, third_values_list), key = (
        values_lists_triplet_with_key
    )
    first_priority_queue = PriorityQueue(
        *first_values_list, key=key, reverse=first_reverse
    )
    second_priority_queue = PriorityQueue(
        *second_values_list, key=key, reverse=second_reverse
    )
    third_priority_queue = PriorityQueue(
        *third_values_list, key=key, reverse=third_reverse
    )
    return first_priority_queue, second_priority_queue, third_priority_queue


priority_queues_triplets = _st.builds(
    to_priority_queues_triplet,
    value_with_key_strategy_strategy.flatmap(
        partial(to_value_sequences_with_key_strategy, sizes=[(0, None)] * 3)
    ),
    booleans,
    booleans,
    booleans,
)
