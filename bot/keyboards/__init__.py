from typing import List

from aiogram.types import InlineKeyboardButton, KeyboardButton

from .base import CommonInlineKeyboard, CommonKeyboard

__all__ = [
    "CommonInlineKeyboard",
    "CommonKeyboard",
]


for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "model_rebuild"):
        continue
    _entity.model_rebuild(
        _types_namespace={
            "List": List,
            "InlineKeyboardButton": InlineKeyboardButton,
            "KeyboardButton": KeyboardButton,
            **{k: v for k, v in globals().items() if k in __all__},
        }
    )

del _entity
del _entity_name
