import math
from functools import partial
from operator import not_

from hypothesis import strategies

from prioq.utils import identity
from .factories import (to_priority_queue,
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
priority_queues = strategies.builds(to_priority_queue,
                                    values_lists_with_keys, booleans)
empty_priority_queues = strategies.builds(to_priority_queue,
                                          empty_values_lists_with_keys,
                                          booleans)
non_empty_priority_queues = strategies.builds(to_priority_queue,
                                              non_empty_values_lists_with_keys,
                                              booleans)
