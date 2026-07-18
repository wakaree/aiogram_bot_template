from dataclasses import dataclass
from typing import Any

from app.domain.user import User
from app.presentation.telegram.flows.base import BaseFlow
from app.presentation.telegram.presenters.common.menu import CommonMenuPresenter
from app.presentation.telegram.view.renderer import Renderer


@dataclass(frozen=True)
class CommonMenuFlow(BaseFlow):
    user: User
    presenter: CommonMenuPresenter
    renderer: Renderer

    async def greeting(self) -> Any:
        return await self.renderer.apply(self.presenter.greeting(user=self.user))

    async def answer_deposit(self) -> Any:
        return await self.renderer.apply(self.presenter.deposit())
