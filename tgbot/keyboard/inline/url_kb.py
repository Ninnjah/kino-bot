from functools import cache

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.models.url import Url


@cache
def get(*urls: Url) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=x.text, url=x.url)]
            for x in urls
        ]
    )
