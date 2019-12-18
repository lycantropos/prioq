from operator import itemgetter
from typing import (List,
                    Optional,
                    Sequence,
                    Tuple)

from hypothesis import strategies

from prioq.hints import (Domain,
                         Key,
                         Range)
from tests.utils import Strategy


def to_values_tuples_with_keys(
        values_with_keys: Strategy[Tuple[Strategy[Domain],
                                         Strategy[Key]]]
) -> Strategy[Tuple[Strategy[Tuple[Domain, ...]], Strategy[Key]]]:
    def to_values_tuples_with_key(
            values_with_keys_list: List[Strategy[Tuple[Domain, Key]]]
    ) -> Tuple[Strategy[Tuple[Domain, ...]], Strategy[Key]]:
        def combine_keys(keys: Tuple[Key, ...]) -> Key:
            def combined(values: Sequence[Domain]) -> Range:
                return tuple(key(arg) for key, arg in zip(keys, values))

            name = ('combination_of_' + '_'.join(key.__qualname__
                                                 for key in keys)
                    if keys else 'empty_combination')
            combined.__name__ = combined.__qualname__ = name
            return combined

        return (strategies.tuples(*map(itemgetter(0), values_with_keys_list)),
                strategies.tuples(*map(itemgetter(1), values_with_keys_list))
                .map(combine_keys))

    return (strategies.lists(values_with_keys,
                             max_size=100)
            .map(to_values_tuples_with_key))


def to_values_with_keys(values_with_keys: Tuple[Strategy[Domain],
                                                Strategy[Key]]
                        ) -> Strategy[Tuple[Domain, Optional[Key]]]:
    values, keys = values_with_keys
    return strategies.tuples(values, strategies.none() | keys)


def to_values_lists_with_keys(
        values_with_keys: Tuple[Strategy[Domain], Strategy[Key]],
        *,
        sizes: Sequence[Tuple[int, Optional[int]]] = ((0, None),)
) -> Strategy[Tuple[List[Domain], Optional[Key]]]:
    values, keys = values_with_keys
    lists_strategies = [strategies.lists(values,
                                         min_size=min_size,
                                         max_size=max_size)
                        for min_size, max_size in sizes]
    return strategies.tuples(*lists_strategies, strategies.none() | keys)
