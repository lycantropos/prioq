from functools import partial
from operator import itemgetter
from typing import (List,
                    Optional,
                    Sequence,
                    Tuple)

from hypothesis import strategies

from prioq.base import PriorityQueue
from prioq.hints import (Key,
                         SortingKey,
                         Value)
from tests.utils import Strategy


def to_values_tuples_with_keys(
        values_with_keys: Strategy[Tuple[Strategy[Value],
                                         Strategy[SortingKey]]]
) -> Strategy[Tuple[Strategy[Tuple[Value, ...]], Strategy[SortingKey]]]:
    def to_values_tuples_with_key(
            values_with_keys_list: List[Strategy[Tuple[Value, SortingKey]]]
    ) -> Tuple[Strategy[Tuple[Value, ...]], Strategy[SortingKey]]:
        def combine_keys(keys: Sequence[SortingKey]) -> SortingKey:
            return partial(combined, keys)

        return (strategies.tuples(*map(itemgetter(0), values_with_keys_list)),
                strategies.tuples(*map(itemgetter(1), values_with_keys_list))
                .map(combine_keys))

    return (strategies.lists(values_with_keys,
                             max_size=100)
            .map(to_values_tuples_with_key))


def combined(keys: Sequence[SortingKey], values: Sequence[Value]) -> Key:
    return tuple(key(arg) for key, arg in zip(keys, values))


def to_values_with_keys(values_with_keys: Tuple[Strategy[Value],
                                                Strategy[SortingKey]]
                        ) -> Strategy[Tuple[Value, Optional[SortingKey]]]:
    values, keys = values_with_keys
    return strategies.tuples(values, strategies.none() | keys)


def to_values_lists_with_keys(
        values_with_keys: Tuple[Strategy[Value], Strategy[SortingKey]],
        *,
        sizes: Sequence[Tuple[int, Optional[int]]] = ((0, None),)
) -> Strategy[Tuple[List[Value], Optional[SortingKey]]]:
    values, keys = values_with_keys
    lists_strategies = [strategies.lists(values,
                                         min_size=min_size,
                                         max_size=max_size)
                        for min_size, max_size in sizes]
    return strategies.tuples(*lists_strategies, strategies.none() | keys)


def to_priority_queue(values_with_key: Tuple[List[Value],
                                             Optional[SortingKey]],
                      reverse: bool) -> PriorityQueue:
    values, key = values_with_key
    return PriorityQueue(*values,
                         key=key,
                         reverse=reverse)


def to_priority_queue_with_value(values_with_key: Tuple[List[Value],
                                                        Optional[SortingKey]],
                                 reverse: bool
                                 ) -> Tuple[PriorityQueue, Value]:
    values, key = values_with_key
    value, *rest_values = values
    return (PriorityQueue(*rest_values,
                          key=key,
                          reverse=reverse),
            value)


def to_priority_queues_with_their_values(queue: PriorityQueue
                                         ) -> Strategy[Tuple[PriorityQueue,
                                                             Value]]:
    return strategies.tuples(strategies.just(queue),
                             strategies.sampled_from(list(queue)))
