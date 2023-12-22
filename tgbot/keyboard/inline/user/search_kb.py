from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number

from tgbot.services.film_api.models import Film


class SearchCallback(CallbackData, prefix="s"):
    film_id: int


def get(l10n: FluentLocalization, films: List[Film]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for film in films:
        builder.button(
            text=l10n.format_value(
                "search-button-text",
                dict(
                    title=film.name_ru or film.name_en,
                    rating=film.rating,
                    year=fluent_number(film.year, useGrouping=False),
                ),
            ),
            callback_data=SearchCallback(film_id=film.film_id),
        )

    builder.adjust(1)

    return builder.as_markup()
