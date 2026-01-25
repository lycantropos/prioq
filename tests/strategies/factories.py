from collections.abc import Callable, Sequence
from functools import partial

from hypothesis import strategies as st

from prioq.base import PriorityQueue
from tests.hints import KeyT, ValueT


def to_values_tuples_with_keys(
    values_with_keys: st.SearchStrategy[
        tuple[
            st.SearchStrategy[ValueT],
            st.SearchStrategy[Callable[[ValueT], KeyT]],
        ]
    ],
    /,
) -> st.SearchStrategy[
    tuple[
        st.SearchStrategy[tuple[ValueT, ...]],
        st.SearchStrategy[Callable[[Sequence[ValueT]], tuple[KeyT, ...]]],
    ]
]:
    def to_value_tuple_with_key_strategies(
        value_with_key_strategies: list[
            tuple[
                st.SearchStrategy[ValueT],
                st.SearchStrategy[Callable[[ValueT], KeyT]],
            ]
        ],
        /,
    ) -> tuple[
        st.SearchStrategy[tuple[ValueT, ...]],
        st.SearchStrategy[Callable[[Sequence[ValueT]], tuple[KeyT, ...]]],
    ]:
        def combine_keys(
            keys: tuple[Callable[[ValueT], KeyT], ...], /
        ) -> Callable[[Sequence[ValueT]], tuple[KeyT, ...]]:
            return partial(to_combined_keys, keys)

        return (
            st.tuples(
                *[
                    value_strategy
                    for value_strategy, _ in value_with_key_strategies
                ]
            ),
            st.tuples(
                *[
                    key_strategy
                    for _, key_strategy in value_with_key_strategies
                ]
            ).map(combine_keys),
        )

    return st.lists(values_with_keys, max_size=100).map(
        to_value_tuple_with_key_strategies
    )


def to_combined_keys(
    keys: Sequence[Callable[[ValueT], KeyT]], values: Sequence[ValueT], /
) -> tuple[KeyT, ...]:
    return tuple(key(arg) for key, arg in zip(keys, values, strict=True))


def to_value_with_key_strategy(
    values_with_keys: tuple[
        st.SearchStrategy[ValueT],
        st.SearchStrategy[Callable[[ValueT], KeyT] | None],
    ],
    /,
) -> st.SearchStrategy[tuple[ValueT, Callable[[ValueT], KeyT] | None]]:
    values, keys = values_with_keys
    return st.tuples(values, keys)


def to_value_sequence_with_key_strategy(
    value_with_key_strategy: tuple[
        st.SearchStrategy[ValueT],
        st.SearchStrategy[Callable[[ValueT], KeyT] | None],
    ],
    /,
    min_size: int = 0,
    max_size: int | None = None,
) -> st.SearchStrategy[
    tuple[Sequence[ValueT], Callable[[ValueT], KeyT] | None]
]:
    value_strategy, key_strategy = value_with_key_strategy
    return st.tuples(
        st.lists(value_strategy, min_size=min_size, max_size=max_size),
        key_strategy,
    )


def to_value_sequences_with_key_strategy(
    value_with_key_strategy: tuple[
        st.SearchStrategy[ValueT],
        st.SearchStrategy[Callable[[ValueT], KeyT] | None],
    ],
    /,
    *,
    sizes: Sequence[tuple[int, int | None]],
) -> st.SearchStrategy[
    tuple[Sequence[Sequence[ValueT]], Callable[[ValueT], KeyT] | None]
]:
    value_strategy, key_strategy = value_with_key_strategy
    return st.tuples(
        st.tuples(
            *[
                st.lists(value_strategy, min_size=min_size, max_size=max_size)
                for min_size, max_size in sizes
            ]
        ),
        key_strategy,
    )


def to_priority_queue(
    values_with_key: tuple[list[ValueT], Callable[[ValueT], KeyT] | None],
    reverse: bool,
    /,
) -> PriorityQueue[KeyT, ValueT]:
    values, key = values_with_key
    return PriorityQueue(*values, key=key, reverse=reverse)


def to_priority_queue_with_value(
    values_with_key: tuple[list[ValueT], Callable[[ValueT], KeyT] | None],
    reverse: bool,
    /,
) -> tuple[PriorityQueue[KeyT, ValueT], ValueT]:
    values, key = values_with_key
    value, *rest_values = values
    return PriorityQueue(*rest_values, key=key, reverse=reverse), value


def to_priority_queue_with_their_value_strategy(
    queue: PriorityQueue[KeyT, ValueT], /
) -> st.SearchStrategy[tuple[PriorityQueue[KeyT, ValueT], ValueT]]:
    return st.tuples(st.just(queue), st.sampled_from(queue.values()))
