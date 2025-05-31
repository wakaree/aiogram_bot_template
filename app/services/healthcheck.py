from typing import Any

from aiogram import Dispatcher

from app.models.dto.healthcheck import CheckerResult, HealthcheckResponse
from app.services.redis import RedisRepository


async def check_redis(response: HealthcheckResponse, redis: RedisRepository) -> None:
    try:
        redis_response: Any = await redis.client.ping()
        response.results.append(
            CheckerResult(
                name="redis",
                ok=True,
                message=str(redis_response),
            ),
        )
    except Exception as error:
        response.results.append(
            CheckerResult(
                name="redis",
                ok=False,
                message=str(error),
            ),
        )


def check_polling(response: HealthcheckResponse, dispatcher: Dispatcher) -> None:
    if dispatcher._running_lock.locked():
        response.results.append(
            CheckerResult(name="polling", ok=True, message="Polling is running")
        )
        return
    response.results.append(
        CheckerResult(name="polling", ok=False, message="Polling is not running")
    )
