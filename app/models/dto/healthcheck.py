from typing import Self

from pydantic import Field

from app.models.base import PydanticModel
from app.utils.time import get_uptime


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
