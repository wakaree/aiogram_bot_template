from __future__ import annotations

from typing import Any, Self

from aiogram import Dispatcher
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, Response
from pydantic import Field

from app.application.models.base import PydanticModel
from app.infrastructure.redis.repository import RedisRepository
from app.utils.time import get_uptime

router: APIRouter = APIRouter(prefix="/health")


class CheckerResult(PydanticModel):
    name: str
    ok: bool
    message: str


class HealthcheckResponse(PydanticModel):
    uptime: int = Field(default_factory=get_uptime)
    ok: bool = True
    results: list[CheckerResult] = Field(default_factory=list)

    def actualize_ok(self) -> None:
        self.ok = all(result.ok for result in self.results)

    def get_status_code(self) -> int:
        self.actualize_ok()
        return 200 if self.ok else 503

    @classmethod
    def alive(cls, service: str) -> Self:
        return cls(
            results=[
                CheckerResult(
                    name="service",
                    ok=True,
                    message=f"{service.capitalize()} service is alive",
                ),
            ],
        )

    @classmethod
    def ready(cls, service: str, ready: bool) -> Self:
        not_: str = "not " if not ready else ""
        return cls(
            results=[
                CheckerResult(
                    name="service",
                    ok=ready,
                    message=f"{service.capitalize()} service is {not_}ready",
                ),
            ],
        )


async def check_redis(response: HealthcheckResponse, redis: RedisRepository) -> None:
    try:
        redis_response: Any = await redis.client.ping()
        response.results.append(
            CheckerResult(name="redis", ok=True, message=str(redis_response)),
        )
    except Exception as error:  # noqa: BLE001
        response.results.append(CheckerResult(name="redis", ok=False, message=str(error)))


def check_polling(response: HealthcheckResponse, dispatcher: Dispatcher) -> None:
    if dispatcher._running_lock.locked():
        response.results.append(
            CheckerResult(name="polling", ok=True, message="Polling is running"),
        )
        return
    response.results.append(
        CheckerResult(name="polling", ok=False, message="Polling is not running"),
    )


@router.get(path="/liveness")
async def handle_liveness() -> HealthcheckResponse:
    return HealthcheckResponse.alive(service="bot")


@router.get(path="/readiness")
@inject
async def handle_readiness(
    request: Request,
    response: Response,
    redis: FromDishka[RedisRepository],
) -> HealthcheckResponse:
    response_body: HealthcheckResponse = HealthcheckResponse.ready(service="bot", ready=True)
    if request.app.state.shutdown_completed:
        response_body = HealthcheckResponse.ready(service="bot", ready=False)
    else:
        await check_redis(response=response_body, redis=redis)
    response.status_code = response_body.get_status_code()
    return response_body
