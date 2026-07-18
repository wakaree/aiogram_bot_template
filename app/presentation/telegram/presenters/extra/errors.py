from dataclasses import dataclass

from aiogram_i18n import I18nContext

from app.presentation.telegram.presenters.base import BasePresenter
from app.presentation.telegram.view.models import View


@dataclass(frozen=True)
class ExtraErrorsPresenter(BasePresenter):
    i18n: I18nContext

    def something_went_wrong(self) -> View:
        return View(text=self.i18n.messages.errors.something_went_wrong())
