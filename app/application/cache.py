from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Coroutine, Protocol, cast

from app.application.ports.storages.cache import Cache


class HasCache(Protocol):
    _cache: Cache


@dataclass(frozen=True)
class CacheMeta:
    """Плоские метаданные @cache-вызова — без TypeAdapter/сериализации.

    Реализация ``Cache`` (инфраструктура) сама решает, как по ``func`` достать тип
    возврата и провалидировать значение — здесь про это ничего не знают.
    """

    func: Callable[..., Any]
    prefix: str | None
    ttl: int


def cache[T, **P](
    *,
    prefix: str | None = None,
    ttl: int,
) -> Callable[[Callable[P, Coroutine[Any, Any, T]]], Callable[P, Coroutine[Any, Any, T]]]:
    """Cache a method's return value behind the injected ``Cache`` port.

    Знает только про наличие ``self._cache`` — ничего не знает про pydantic,
    сериализацию или то, куда физически пишется кэш (это дело реализации порта).
    """

    def decorator(
        func: Callable[P, Coroutine[Any, Any, T]],
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            self: HasCache = cast(HasCache, args[0])
            return await self._cache.cached_call(func, ttl, prefix, *args, **kwargs)

        wrapper._cache_meta = CacheMeta(func=func, prefix=prefix, ttl=ttl)  # type: ignore[attr-defined]
        return wrapper

    return decorator


def epoch_cache[T, **P](
    *,
    prefix: str | None = None,
    ttl: int,
    epoch_prefix: str,
    epoch_fields: list[str],
) -> Callable[[Callable[P, Coroutine[Any, Any, T]]], Callable[P, Coroutine[Any, Any, T]]]:
    def decorator(
        func: Callable[P, Coroutine[Any, Any, T]],
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            self: HasCache = cast(HasCache, args[0])
            return await self._cache.epoch_cached_call(
                func,
                ttl,
                epoch_prefix,
                epoch_fields,
                prefix,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator
