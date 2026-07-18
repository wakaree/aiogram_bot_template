from functools import partial
from typing import Any, Callable, Coroutine, Literal, Optional, Protocol


class Cache(Protocol):
    async def cached_call[T, **P](
        self,
        func: Callable[P, Coroutine[Any, Any, T]],
        ttl: int,
        prefix: Optional[str] = None,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T: ...

    async def cached_batch(self, *specs: partial[Coroutine[Any, Any, Any]]) -> list[Any]:
        """Resolve N @cache-decorated calls in a single MGET + pipelined writeback.

        Each spec is ``partial(bound_method, ...)`` where ``bound_method`` is already
        decorated with :func:`app.application.cache.cache`.
        """
        ...

    async def epoch_cached_call[T, **P](
        self,
        func: Callable[P, Coroutine[Any, Any, T]],
        ttl: int,
        epoch_prefix: str,
        epoch_fields: list[str],
        prefix: Optional[str] = None,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T: ...

    async def invalidate(self, prefix: str, kwargs: dict[str, Any]) -> None: ...

    async def bump_epoch(
        self,
        epoch_prefix: str,
        epoch_values: list[Any],
        mode: Literal["incr", "random", "timestamp"] = "random",
        ttl_seconds: Optional[int] = None,
    ) -> str: ...
