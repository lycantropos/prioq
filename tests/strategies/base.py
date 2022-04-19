import math
from functools import partial
from operator import not_

from hypothesis import strategies

from prioq.base import PriorityQueue
from tests.utils import (PriorityQueuesPair,
                         PriorityQueuesTriplet,
                         ValuesListsPairWithKey,
                         ValuesListsTripletWithKey,
                         identity)
from .factories import (to_priority_queue,
                        to_priority_queue_with_value,
                        to_priority_queues_with_their_values,
                        to_values_lists_with_keys,
                        to_values_tuples_with_keys,
                        to_values_with_keys)

booleans = strategies.booleans()
maybe_infinite_numbers_keys = strategies.sampled_from([identity, abs])
finite_numbers_keys = (maybe_infinite_numbers_keys
                       | strategies.sampled_from([round, math.trunc, math.ceil,
                                                  math.floor]))
strings_keys = strategies.sampled_from([identity, str.lower, str.upper,
                                        str.title, str.capitalize,
                                        str.casefold, str.swapcase])

base_values_with_keys_strategies = strategies.sampled_from(
        [(strategies.integers(), finite_numbers_keys),
         (strategies.floats(allow_nan=False), maybe_infinite_numbers_keys),
         (strategies.floats(allow_nan=False,
                            allow_infinity=False),
          finite_numbers_keys),
         (strategies.booleans(), strategies.just(not_) | finite_numbers_keys),
         (strategies.text(), strings_keys)])
values_with_keys_strategies = (strategies
                               .recursive(base_values_with_keys_strategies,
                                          to_values_tuples_with_keys,
                                          max_leaves=10))
values_with_keys = values_with_keys_strategies.flatmap(to_values_with_keys)
values_lists_with_keys = (values_with_keys_strategies
                          .flatmap(to_values_lists_with_keys))
empty_values_lists_with_keys = (values_with_keys_strategies
                                .flatmap(partial(to_values_lists_with_keys,
                                                 sizes=[(0, 0)])))
non_empty_values_lists_with_keys = (values_with_keys_strategies
                                    .flatmap(partial(to_values_lists_with_keys,
                                                     sizes=[(1, None)])))
single_values_with_keys = (values_with_keys_strategies
                           .flatmap(partial(to_values_lists_with_keys,
                                            sizes=[(1, 1)])))
priority_queues = strategies.builds(to_priority_queue,
                                    values_lists_with_keys, booleans)
empty_priority_queues = strategies.builds(to_priority_queue,
                                          empty_values_lists_with_keys,
                                          booleans)
non_empty_priority_queues = strategies.builds(to_priority_queue,
                                              non_empty_values_lists_with_keys,
                                              booleans)
priority_queues_with_values = strategies.builds(
        to_priority_queue_with_value, non_empty_values_lists_with_keys,
        booleans)
empty_priority_queues_with_values = strategies.builds(
        to_priority_queue_with_value, single_values_with_keys, booleans)
non_empty_priority_queues_with_their_values = (
    non_empty_priority_queues.flatmap(to_priority_queues_with_their_values))


def to_priority_queues_pair(values_lists_pair_with_key: ValuesListsPairWithKey,
                            first_reverse: bool,
                            second_reverse: bool) -> PriorityQueuesPair:
    first_values_list, second_values_list, key = values_lists_pair_with_key
    first_priority_queue = PriorityQueue(*first_values_list,
                                         key=key,
                                         reverse=first_reverse)
    second_priority_queue = PriorityQueue(*second_values_list,
                                          key=key,
                                          reverse=second_reverse)
    return first_priority_queue, second_priority_queue


priority_queues_pairs = strategies.builds(
        to_priority_queues_pair,
        values_with_keys_strategies.flatmap(partial(to_values_lists_with_keys,
                                                    sizes=[(0, None)] * 2)),
        booleans, booleans)


def to_priority_queues_triplet(
        values_lists_triplet_with_key: ValuesListsTripletWithKey,
        first_reverse: bool,
        second_reverse: bool,
        third_reverse: bool) -> PriorityQueuesTriplet:
    (first_values_list, second_values_list,
     third_values_list, key) = values_lists_triplet_with_key
    first_priority_queue = PriorityQueue(*first_values_list,
                                         key=key,
                                         reverse=first_reverse)
    second_priority_queue = PriorityQueue(*second_values_list,
                                          key=key,
                                          reverse=second_reverse)
    third_priority_queue = PriorityQueue(*third_values_list,
                                         key=key,
                                         reverse=third_reverse)
    return first_priority_queue, second_priority_queue, third_priority_queue


priority_queues_triplets = strategies.builds(
        to_priority_queues_triplet,
        values_with_keys_strategies.flatmap(partial(to_values_lists_with_keys,
                                                    sizes=[(0, None)] * 3)),
        booleans, booleans, booleans)
