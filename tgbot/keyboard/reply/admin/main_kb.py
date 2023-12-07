from functools import cache

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from fluent.runtime import FluentLocalization


@cache
def get(l10n: FluentLocalization):
    keyboard = [
        [KeyboardButton(text=l10n.format_value("admin-list-user-button-text"))],
        [KeyboardButton(text=l10n.format_value("admin-list-admin-button-text"))],
        [
            KeyboardButton(text=l10n.format_value("admin-add-admin-button-text")),
            KeyboardButton(text=l10n.format_value("admin-delete-admin-button-text")),
        ],
        [KeyboardButton(text=l10n.format_value("admin-list-players-button-text"))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
