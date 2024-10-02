from ..base import FromAttributesModel


class UserDto(FromAttributesModel):
    id: int
    telegram_id: int
    name: str
    locale: str
    bot_blocked: bool
