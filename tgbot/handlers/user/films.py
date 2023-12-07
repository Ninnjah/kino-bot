import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, URLInputFile
from aiogram.utils.chat_action import ChatActionSender

from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from tgbot.keyboard.inline import url_kb
from tgbot.keyboard.inline.user import search_kb
from tgbot.services.repository import Repo
from tgbot.services.film_api import KinopoiskAPI
from tgbot.services.film_api import players as players_
from tgbot.services.film_api.models.films import Search

router = Router(name=__name__)


async def search_films(
    m: Message, 
    l10n: FluentLocalization,
    pool: AsyncEngine, 
    search: Search,
):
    async with ChatActionSender.typing(bot=m.bot, chat_id=m.chat.id):
        async with pool.connect() as conn:
            repo = Repo(conn)
            players_conf = [x.title for x in await repo.list_players() if x.is_active]
            players = [x for x in players_ if x.title in players_conf]
            players_count = len(players)
            
            available_films = await repo.list_films([x.film_id for x in search.films])
            needed_films = [
                x for x in available_films
                if any((
                    any([x.film_id == y.film_id for y in search.films]),
                    len(x.source) < players_count if x.source else False,
                ))
            ]
            await repo.add_film(search.films)
            
            for player in players:
                needed_source = [
                    x for x in needed_films 
                    if not x.source 
                    or player.title not in [y.title for y in x.source]
                ]
                
                sources = await player.get_bunch_source(needed_source)
                available_films += [x for x in search.films if x.film_id in [y.film_id for y in sources]]
                if sources:
                    await repo.add_source(sources)

            available_films = await repo.search_films([film.film_id for film in search.films])
            films = [x for x in search.films if x.film_id in [y.film_id for y in available_films]]
            await m.edit_text(
                l10n.format_value("search-message-text", dict(request=search.keyword)),
                reply_markup=search_kb.get(l10n, films)
            )


@router.message(F.text)
async def search_film_handler(
    m: Message, 
    l10n: FluentLocalization,
    repo: Repo, 
    pool: AsyncEngine,
    kinopoisk: KinopoiskAPI,
):
    await m.bot.send_chat_action(m.chat.id, "typing")

    search = await kinopoisk.films_search_by_keyword(m.text)  
    if not search:
        await m.answer(l10n.format_value("search-not-found-text"))
        return

    msg = await m.answer(l10n.format_value("search-wait-text"))
    asyncio.create_task(search_films(m=msg, l10n=l10n, pool=pool, search=search))


@router.callback_query(search_kb.SearchCallback.filter())
async def film_handler(
    callback: CallbackQuery, 
    callback_data: search_kb.SearchCallback, 
    l10n: FluentLocalization, 
    repo: Repo,
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
