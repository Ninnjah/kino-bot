from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, URLInputFile
from aiogram.utils.deep_linking import create_start_link

from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number

from tgbot.keyboard.inline.user import film_kb
from tgbot.services.repository import Repo

router = Router(name=__name__)


@router.message(CommandStart(deep_link=True))
async def share_film(
    m: Message, command: CommandObject, l10n: FluentLocalization, repo: Repo
):
    try:
        film_id = int(command.args)
        film = await repo.get_film(film_id)
        if not film or not film.source:
            raise ValueError

    except ValueError:
        await m.answer(l10n.format_value("film-not-found-text"))
        return

    else:
        await m.answer_photo(
            URLInputFile(film.poster_url.unicode_string()),
            caption=l10n.format_value(
                "film-message-text",
                dict(
                    title=film.name_ru or film.name_en,
                    rating=film.rating,
                    year=fluent_number(film.year, useGrouping=False),
                    genres=", ".join(film.genres),
                    description=film.description,
                    share_url=await create_start_link(m.bot, film.film_id),
                ),
            ),
            reply_markup=film_kb.get(
                l10n=l10n,
                film=film,
            ),
        )


@router.message(Command("start"))
async def start_handler(m: Message, l10n: FluentLocalization, repo: Repo):
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username,
    )
    await m.answer(l10n.format_value("user-start-text"))
