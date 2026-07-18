import hashlib
import inspect
import pickle
from typing import Any, Callable, Iterable


def bind_function_args(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> inspect.BoundArguments:
    sig = inspect.signature(func)
    try:
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        return bound
    except TypeError:
        return sig.bind_partial(*args[: len(sig.parameters)], **kwargs)


def values_by_names(bound: inspect.BoundArguments, names: Iterable[str]) -> list[Any]:
    values: list[Any] = []
    for name in names:
        if name not in bound.arguments:
            raise KeyError(f"Parameter '{name}' not found in {bound.signature}")
        values.append(bound.arguments[name])
    return values


def build_cache_key(
    prefix: str,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    additional: list[str] | None = None,
) -> str:
    data: tuple[Any, ...] = (args, tuple(sorted(kwargs.items())))
    raw_data: bytes = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    args_hash: str = hashlib.blake2b(raw_data, digest_size=16).hexdigest()
    return ":".join([prefix, f"h={args_hash}", *(additional or [])])


def parse_cache_key(
    *,
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    prefix: str | None,
    additional: list[str] | None = None,
) -> str:
    # args[0] — bound `self`, не участвует в ключе.
    return build_cache_key(
        prefix=prefix or func.__name__,
        args=args[1:],
        kwargs=kwargs,
        additional=additional,
    )


def epoch_key(epoch_prefix: str, epoch_values: list[Any]) -> str:
    parts = [epoch_prefix, *map(str, epoch_values), "epoch"]
    return ":".join(parts)
