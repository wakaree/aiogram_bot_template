import asyncio
import logging
import secrets
import time
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Coroutine, Final, Literal, get_type_hints

from pydantic import TypeAdapter, ValidationError
from redis.asyncio import Redis

from app.application.cache import CacheMeta
from app.application.ports.storages.cache import Cache
from app.infrastructure.redis.cache.keys import (
    bind_function_args,
    build_cache_key,
    epoch_key,
    parse_cache_key,
    values_by_names,
)
from app.utils import mjson

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True)
class _CacheRequest:
    cache_key: str
    thunk: Callable[[], Coroutine[Any, Any, Any]]
    ttl: int
    type_adapter: TypeAdapter[Any]


@dataclass
class RedisCache(Cache):
    _redis: Redis

    async def _cached_func_call(
        self,
        cache_key: str,
        thunk: Callable[[], Coroutine[Any, Any, Any]],
        ttl: int,
        type_adapter: TypeAdapter[Any],
    ) -> Any:
        cached_value: Any = await self._redis.get(cache_key)
        if isinstance(cached_value, bytes):
            cached_value = cached_value.decode()

        if cached_value is not None:
            try:
                return type_adapter.validate_python(mjson.decode(cached_value))
            except ValidationError as error:
                logger.error(
                    "Validation error for cached value (%s): %s (key=%s)",
                    type(error).__name__,
                    error,
                    cache_key,
                )
                await self._redis.delete(cache_key)

        result: Any = await thunk()
        try:
            payload = mjson.encode(type_adapter.dump_python(result))
            await self._redis.setex(cache_key, ttl, payload)
        except Exception as error:  # noqa: BLE001
            logger.warning("Failed to set cache for key=%s: %s", cache_key, error)

        return result

    async def cached_call(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        ttl: int,
        prefix: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return_type: Any = get_type_hints(func).get("return", Any)
        type_adapter: TypeAdapter[Any] = TypeAdapter(return_type)
        cache_key: str = parse_cache_key(func=func, args=args, kwargs=kwargs, prefix=prefix)
        thunk: Callable[[], Coroutine[Any, Any, Any]] = partial(func, *args, **kwargs)
        return await self._cached_func_call(cache_key, thunk, ttl, type_adapter)

    def _coerce_request(self, spec: partial[Coroutine[Any, Any, Any]]) -> _CacheRequest:
        bound_method: Any = spec.func
        meta: CacheMeta | None = getattr(bound_method, "_cache_meta", None)
        if meta is None:
            meta = getattr(getattr(bound_method, "__func__", None), "_cache_meta", None)
        if meta is None:
            raise TypeError(
                f"cached_batch expects a @cache-decorated bound method, got {bound_method!r}"
            )

        owner: Any = bound_method.__self__
        args: tuple[Any, ...] = (owner, *spec.args)
        kwargs: dict[str, Any] = dict(spec.keywords or {})

        return_type: Any = get_type_hints(meta.func).get("return", Any)
        type_adapter: TypeAdapter[Any] = TypeAdapter(return_type)
        cache_key: str = parse_cache_key(
            func=meta.func,
            args=args,
            kwargs=kwargs,
            prefix=meta.prefix,
        )
        thunk: Callable[[], Coroutine[Any, Any, Any]] = partial(meta.func, *args, **kwargs)
        return _CacheRequest(
            cache_key=cache_key,
            thunk=thunk,
            ttl=meta.ttl,
            type_adapter=type_adapter,
        )

    def _decode_cached_values(
        self,
        requests: list[_CacheRequest],
        raw_values: list[Any],
    ) -> tuple[list[Any], list[int], list[int]]:
        results: list[Any] = [None] * len(requests)
        misses: list[int] = []
        invalid: list[int] = []
        for i, (request, raw) in enumerate(zip(requests, raw_values)):
            if raw is None:
                misses.append(i)
                continue
            if isinstance(raw, bytes):
                raw = raw.decode()
            try:
                results[i] = request.type_adapter.validate_python(mjson.decode(raw))
            except ValidationError as error:
                logger.error(
                    "Validation error for cached value (%s): %s (key=%s)",
                    type(error).__name__,
                    error,
                    request.cache_key,
                )
                misses.append(i)
                invalid.append(i)
        return results, misses, invalid

    async def _flush_cache_writeback(
        self,
        requests: list[_CacheRequest],
        misses: list[int],
        invalid: list[int],
        fresh_values: list[Any],
    ) -> None:
        try:
            async with self._redis.pipeline(transaction=False) as pipe:
                for idx in invalid:
                    pipe.delete(requests[idx].cache_key)
                for idx, value in zip(misses, fresh_values):
                    request = requests[idx]
                    try:
                        payload = mjson.encode(request.type_adapter.dump_python(value))
                    except Exception as error:  # noqa: BLE001
                        logger.warning(
                            "Failed to encode cache for key=%s: %s",
                            request.cache_key,
                            error,
                        )
                        continue
                    pipe.setex(request.cache_key, request.ttl, payload)
                await pipe.execute()
        except Exception as error:  # noqa: BLE001
            logger.warning("Failed to flush cache pipeline: %s", error)

    async def cached_batch(self, *specs: partial[Coroutine[Any, Any, Any]]) -> list[Any]:
        if not specs:
            return []

        requests: list[_CacheRequest] = [self._coerce_request(spec) for spec in specs]
        keys: list[str] = [request.cache_key for request in requests]

        raw_values: list[Any] = await self._redis.mget(keys)
        results, misses, invalid = self._decode_cached_values(requests, raw_values)

        if not misses:
            return results

        fresh_values: list[Any] = list(
            await asyncio.gather(*(requests[i].thunk() for i in misses)),
        )
        for idx, value in zip(misses, fresh_values):
            results[idx] = value

        await self._flush_cache_writeback(requests, misses, invalid, fresh_values)
        return results

    async def _get_epoch(
        self,
        epoch_prefix: str,
        epoch_values: list[Any],
        default: str = "0",
    ) -> str:
        key: str = epoch_key(epoch_prefix, epoch_values)
        value: Any = await self._redis.get(key)
        if isinstance(value, bytes):
            value = value.decode()
        return value or default

    async def epoch_cached_call(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        ttl: int,
        epoch_prefix: str,
        epoch_fields: list[str],
        prefix: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return_type: Any = get_type_hints(func).get("return", Any)
        type_adapter: TypeAdapter[Any] = TypeAdapter(return_type)

        if not epoch_fields:
            epoch_values: list[Any] = []
        else:
            bound = bind_function_args(func, args, kwargs)
            try:
                epoch_values = values_by_names(bound, epoch_fields)
            except KeyError as error:
                raise RuntimeError(f"epoch_fields error: {error}") from error

        epoch: str = await self._get_epoch(epoch_prefix=epoch_prefix, epoch_values=epoch_values)
        cache_key: str = parse_cache_key(
            func=func,
            args=args,
            kwargs=kwargs,
            prefix=prefix,
            additional=[f"v={epoch}"],
        )
        thunk: Callable[[], Coroutine[Any, Any, Any]] = partial(func, *args, **kwargs)
        return await self._cached_func_call(cache_key, thunk, ttl, type_adapter)

    async def invalidate(self, prefix: str, kwargs: dict[str, Any]) -> None:
        cache_key: str = build_cache_key(prefix=prefix, args=(), kwargs=kwargs)
        await self._redis.delete(cache_key)

    async def bump_epoch(
        self,
        epoch_prefix: str,
        epoch_values: list[Any],
        mode: Literal["incr", "random", "timestamp"] = "random",
        ttl_seconds: int | None = None,
    ) -> str:
        key: str = epoch_key(epoch_prefix, epoch_values)

        if mode == "incr":
            value: int = await self._redis.incr(key)
            return str(value)

        if mode == "random":
            token16: str = secrets.token_bytes(8).hex()
            if ttl_seconds:
                await self._redis.set(key, token16, ex=ttl_seconds)
            else:
                await self._redis.set(key, token16)
            return token16

        if mode == "timestamp":
            now_ms: int = int(time.time() * 1000)
            if ttl_seconds:
                await self._redis.set(key, str(now_ms), ex=ttl_seconds)
            else:
                await self._redis.set(key, str(now_ms))
            return str(now_ms)

        raise ValueError("Unsupported epoch mode")
