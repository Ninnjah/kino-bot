import asyncio
from operator import itemgetter

from aiogram import Bot, Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hide_link

from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.manager.bg_manager import BgManager
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, ListGroup, Url, Back

from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from kinopoisk_api.api import KinopoiskAPI
from kinopoisk_api.models.model import FilmSearchResponse as Search
from tgbot.handlers.user.states.films import FilmSG
from tgbot.keyboard.inline.user import search_kb, film_kb
from tgbot.services.repository import Repo
from tgbot.services.film_api import players as players_
from tgbot.services.l10n_dialog import L10NFormat

router = Router(name=__name__)


async def get_films(dialog_manager: DialogManager, **kwargs):
    l10n: FluentLocalization = dialog_manager.middleware_data["l10n"]
    raw_search = dialog_manager.dialog_data.get("search")
    if not raw_search:
        return []
    search = Search.model_validate(raw_search)

    return {
        "request": search.keyword,
        "films": [
            (
                film.film_id,
                l10n.format_value(
                    "search-button-text",
                    dict(
                        title=film.name_ru or film.name_en,
                        rating=film.rating if film.rating != "None" else "0.0",
                        year=fluent_number(film.year, useGrouping=False)
                        if film.year
                        else "",
                    ),
                ),
            )
            for film in search.films
        ],
    }


async def get_film_data(dialog_manager: DialogManager, **kwargs):
    bot: Bot = dialog_manager.middleware_data["bot"]
    l10n: FluentLocalization = dialog_manager.middleware_data["l10n"]
    repo: Repo = dialog_manager.middleware_data["repo"]
    film_id: int = dialog_manager.dialog_data["film_id"]

    film = await repo.get_film(film_id)
    if not film:
        return

    return {
        "poster": film.poster_url.unicode_string(),
        "title": film.name_ru or film.name_en,
        "rating": film.rating or "0.0",
        "year": fluent_number(film.year, useGrouping=False) if film.year else "",
        "genres": ", ".join(film.genres),
        "description": film.description,
        "share_url": await create_start_link(bot, film.film_id),
        "links": [
            (
                id_,
                l10n.format_value("film-url-button-text", dict(title=source.title)),
                source.url.unicode_string(),
            )
            for id_, source in enumerate(film.source)
        ]
        if film.source
        else [],
    }


async def search_films(pool: AsyncEngine, search: Search) -> Search:
    async with pool.connect() as conn:
        repo = Repo(conn)
        players_conf = [x.title for x in await repo.list_players() if x.is_active]
        players = [x for x in players_ if x.title in players_conf]
        players_count = len(players)

        available_films = await repo.list_films([x.film_id for x in search.films])
        needed_films = [
            x
            for x in available_films
            if any(
                (
                    any([x.film_id == y.film_id for y in search.films]),
                    len(x.source) < players_count if x.source else False,
                )
            )
        ]
        needed_films += [
            x
            for x in search.films
            if x.film_id not in [y.film_id for y in needed_films]
        ]
        await repo.add_film(search.films)

        for player in players:
            needed_source = [
                x
                for x in needed_films
                if not getattr(x, "source", None)
                or player.title not in [y.title for y in x.source]
            ]

            sources = await player.get_bunch_source(needed_source)
            available_films += [
                x for x in search.films if x.film_id in [y.film_id for y in sources]
            ]
            if sources:
                await repo.add_source(sources)

        available_films = await repo.search_films(
            [film.film_id for film in search.films]
        )
        search.films = [
            x for x in search.films if x.film_id in [y.film_id for y in available_films]
        ]

        return search


async def dialog_search_films(
    manager: BgManager,
    pool: AsyncEngine,
    search: Search,
):
    async with ChatActionSender.typing(bot=manager.bot, chat_id=manager.chat.id):
        search = await search_films(pool, search)
    await manager.update(data={"search": search.model_dump(by_alias=True)})


@router.message(F.text)
async def search_film_handler(
    m: Message,
    l10n: FluentLocalization,
    repo: Repo,
    dialog_manager: DialogManager,
    pool: AsyncEngine,
    kinopoisk: KinopoiskAPI,
):
    await m.bot.send_chat_action(m.chat.id, "typing")

    search = await kinopoisk.films.search_by_keyword(m.text.lower())
    if not search:
        await m.answer(l10n.format_value("search-not-found-text"))
        return

    await dialog_manager.start(FilmSG.lst, mode=StartMode.RESET_STACK)
    bg_manager = dialog_manager.bg()
    asyncio.create_task(
        dialog_search_films(manager=bg_manager, l10n=l10n, pool=pool, search=search)
    )


@router.callback_query(search_kb.SearchCallback.filter())
async def film_handler(
    callback: CallbackQuery,
    select: Select,
    manager: DialogManager,
    film_id: str,
):
    manager.dialog_data["film_id"] = int(film_id)
    await manager.next()


@router.inline_query()
async def inline_film_handler(
    inline_query: InlineQuery,
    l10n: FluentLocalization,
    repo: Repo,
    pool: AsyncEngine,
    kinopoisk: KinopoiskAPI,
):
    if not inline_query.query:
        return
    search = await kinopoisk.films.search_by_keyword(inline_query.query.lower())
    if not search:
        await inline_query.answer(
            l10n.format_value("search-not-found-text"), is_personal=True
        )
        return

    search = await search_films(pool, search)
    films = await repo.list_films([film.film_id for film in search.films])

    results = []
    for film in films:
        results.append(
            InlineQueryResultArticle(
                id=str(film.film_id),
                title=l10n.format_value(
                    "search-button-text",
                    dict(
                        title=film.name_ru or film.name_en,
                        rating=film.rating or "0.0",
                        year=fluent_number(film.year, useGrouping=False)
                        if film.year
                        else "",
                    ),
                ),
                description=film.description,
                thumbnail_url=film.poster_url_preview.unicode_string(),
                input_message_content=InputTextMessageContent(
                    message_text=hide_link(film.poster_url.unicode_string())
                    + l10n.format_value(
                        "film-message-text",
                        dict(
                            title=film.name_ru or film.name_en,
                            rating=film.rating or "0.0",
                            year=fluent_number(film.year, useGrouping=False)
                            if film.year
                            else "",
                            genres=", ".join(film.genres),
                            description=film.description,
                        ),
                    ),
                    parse_mode="HTML",
                ),
                reply_markup=film_kb.get(l10n=l10n, film=film),
            )
        )

    await inline_query.answer(results, is_personal=True)


films_dialog = Dialog(
    Window(
        L10NFormat(
            "search-wait-text",
            when=F["dialog_data"].get("search").is_(None),
        ),
        L10NFormat(
            "search-message-text",
            when="films",
        ),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                id="film_select",
                item_id_getter=itemgetter(0),
                items="films",
                on_click=film_handler,
                when="films",
            ),
            id="film_sg",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        getter=get_films,
        state=FilmSG.lst,
    ),
    Window(
        StaticMedia(url=Format("{poster}")),
        L10NFormat("film-message-text"),
        ListGroup(
            Url(
                Format("{item[1]}"),
                url=Format("{item[2]}"),
            ),
            id="film_links",
            item_id_getter=itemgetter(0),
            items="links",
        ),
        Url(
            L10NFormat("film-share-text"),
            url=L10NFormat("film-share-url"),
            id="share",
        ),
        Back(L10NFormat("admin-button-back")),
        getter=get_film_data,
        state=FilmSG.film,
    ),
)


router.include_routers(
    films_dialog,
)
