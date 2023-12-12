from typing import Optional, Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization


class YesNoCallback(CallbackData, prefix="yn"):
    action: bool
    data: Optional[Union[str, int, float]]


def get(
    l10n: FluentLocalization, data: Optional[Union[str, int, float]] = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=l10n.format_value("yesno-button-text-yes"),
        callback_data=YesNoCallback(action=True, data=data),
    )
    builder.button(
        text=l10n.format_value("yesno-button-text-no"),
        callback_data=YesNoCallback(action=False, data=data),
    )

    builder.adjust(2)

    return builder.as_markup()
