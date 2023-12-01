from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, URLInputFile

from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number

from tgbot.keyboard.inline import url_kb
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


@router.callback_query(search_kb.SearchCallback.filter())
async def film_handler(
    callback: CallbackQuery, 
    callback_data: search_kb.SearchCallback, 
    l10n: FluentLocalization, 
    repo: Repo,
    player: PlayerAPI,
):
    await callback.answer()
    film = await repo.get_film(callback_data.film_id)
    if not film:
        await callback.bot.send_chat_action(callback.message.chat.id, "typing")
        film = await player.get_film_data(callback_data.film_id)
        await repo.add_film(film)

    await callback.message.answer_photo(
        URLInputFile(film.poster_url.unicode_string()),
        caption=l10n.format_value(
            "film-message-text",
            dict(
                title=film.name_ru or film.name_en,
                rating=film.rating,
                year=fluent_number(film.year, useGrouping=False),
                genres=", ".join(film.genres),
            )
        ),
        reply_markup=url_kb.get(
            url_kb.Url(
                text=l10n.format_value("film-url-button-text"),
                url=film.url
            )
        )
    )
