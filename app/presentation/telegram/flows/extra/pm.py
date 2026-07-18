from dataclasses import dataclass

from app.application.interactors.pm.user_status import PMInteractor
from app.presentation.telegram.flows.base import BaseFlow


@dataclass(frozen=True)
class PMFlow(BaseFlow):
    interactor: PMInteractor

    async def mark_blocked(self) -> None:
        await self.interactor.mark_blocked()

    async def mark_unblocked(self) -> None:
        await self.interactor.mark_unblocked()
