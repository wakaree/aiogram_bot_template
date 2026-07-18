from dataclasses import dataclass
from typing import Any

from app.presentation.telegram.flows.base import BaseFlow
from app.presentation.telegram.presenters.extra.errors import ExtraErrorsPresenter
from app.presentation.telegram.view.renderer import Renderer


@dataclass(frozen=True)
class ExtraErrorsFlow(BaseFlow):
    presenter: ExtraErrorsPresenter
    renderer: Renderer

    async def answer_something_went_wrong(self) -> Any:
        return await self.renderer.apply(self.presenter.something_went_wrong())
