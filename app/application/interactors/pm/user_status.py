from dataclasses import dataclass

from app.application.interactors.base import BaseInteractor
from app.application.ports.repositories.users import UsersGateway
from app.domain.user import User
from app.utils.time import datetime_now


@dataclass(frozen=True)
class PMInteractor(BaseInteractor):
    user: User
    users_gateway: UsersGateway

    async def mark_blocked(self) -> None:
        self.user.blocked_at = datetime_now()
        await self.users_gateway.save(self.user)

    async def mark_unblocked(self) -> None:
        self.user.blocked_at = None
        await self.users_gateway.save(self.user)
