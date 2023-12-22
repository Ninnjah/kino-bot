from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization

from tgbot.services.film_api.models import Film


class FilmShareCallback(CallbackData, prefix="share"):
    film_id: int


def get(l10n: FluentLocalization, film: Film) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for source in film.source:
        builder.button(
            text=l10n.format_value("film-url-button-text", dict(title=source.title)),
            url=source.url.unicode_string(),
        )

    builder.adjust(1)

    return builder.as_markup()
