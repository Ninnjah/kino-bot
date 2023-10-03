from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

from tgbot.keyboard.inline.user import search_kb
from tgbot.services.repository import Repo
from tgbot.services.film_api.kinopoisk_api import KinopoiskAPI
from tgbot.services.film_api.player_api import PlayerAPI

router = Router(name=__name__)


@router.message(F.text)
async def search_film_handler(m: Message, l10n: FluentLocalization, kinopoisk: KinopoiskAPI, player: PlayerAPI):
    await m.bot.send_chat_action(m.chat.id, "typing")

    search = await kinopoisk.films_search_by_keyword(m.text)
    available = await player.check_available(search.films)
    available_films = [x for x in search.films if x.film_id in [y.film_id for y in available]]

    await m.answer(
        l10n.format_value("search-message-text", dict(request=m.text)),
        reply_markup=search_kb.get(l10n, available_films)
    )
