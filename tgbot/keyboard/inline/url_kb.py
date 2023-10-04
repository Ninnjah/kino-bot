from functools import cache

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pydantic import BaseModel, AnyUrl


class Url(BaseModel):
    __hash__ = object.__hash__
    text: str
    url: AnyUrl


@cache
def get(*urls: Url) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=x.text, url=x.url.unicode_string())]
            for x in urls
        ]
    )
