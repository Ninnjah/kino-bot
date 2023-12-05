from typing import List

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, URLInputFile

from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number

from tgbot.keyboard.inline import url_kb
from tgbot.keyboard.inline.user import search_kb
from tgbot.services.repository import Repo
from tgbot.services.film_api.kinopoisk_api import KinopoiskAPI
from tgbot.services.film_api.player_api import BasePlayer

router = Router(name=__name__)


@router.message(F.text)
async def search_film_handler(
    m: Message, 
    l10n: FluentLocalization,
    repo: Repo, 
    kinopoisk: KinopoiskAPI, 
    players: List[BasePlayer]
):
    await m.bot.send_chat_action(m.chat.id, "typing")

    search = await kinopoisk.films_search_by_keyword(m.text)  
    if not search:
        await m.answer(l10n.format_value("search-not-found-text"))
        return
    
    available_films = await repo.list_films()
    needed_films = [x for x in search.films if x.film_id not in [y.film_id for y in available_films]]
    await repo.add_film(search.films)
    
    if needed_films:
        for player in players:
            sources = await player.get_bunch_source([
                x for x in needed_films if not x.source or (x.source and x.source.title != player.title)
            ])
            available_films += [x for x in search.films if x.film_id in [y.film_id for y in sources]]
            if sources:
                await repo.add_source(sources)

    available_films = await repo.search_films([film.film_id for film in search.films])
    films = [x for x in search.films if x.film_id in [y.film_id for y in available_films]]
    await m.answer(
        l10n.format_value("search-message-text", dict(request=m.text)),
        reply_markup=search_kb.get(l10n, films)
    )


@router.callback_query(search_kb.SearchCallback.filter())
async def film_handler(
    callback: CallbackQuery, 
    callback_data: search_kb.SearchCallback, 
    l10n: FluentLocalization, 
    repo: Repo,
    players: List[BasePlayer],
):
    await callback.answer()
    film = await repo.get_film(callback_data.film_id)
    if not film or not film.source:
        await callback.answer(l10n.format_value("film-not-found-text"), show_alert=True)
        return

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
        reply_markup=url_kb.get(*[
            url_kb.Url(
                text=l10n.format_value("film-url-button-text", dict(title=source.title)),
                url=source.url
            ) for source in film.source
        ])
    )
