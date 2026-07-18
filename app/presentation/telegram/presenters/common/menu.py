from __future__ import annotations

from dataclasses import dataclass

from aiogram_i18n import I18nContext

from app.domain.user import User
from app.presentation.telegram.keyboards.common import back_keyboard
from app.presentation.telegram.keyboards.menu import deposit_keyboard
from app.presentation.telegram.presenters.base import BasePresenter
from app.presentation.telegram.view.models import View


@dataclass(frozen=True)
class CommonMenuPresenter(BasePresenter):
    i18n: I18nContext

    def greeting(self, user: User) -> View:
        return View(
            text=self.i18n.messages.greeting(name=user.mention),
            reply_markup=deposit_keyboard(i18n=self.i18n),
        )

    def deposit(self) -> View:
        return View(
            text=self.i18n.messages.deposit(),
            reply_markup=back_keyboard(i18n=self.i18n),
        )
