import random

from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, URLInputFile
from aiogram.utils.deep_linking import create_start_link

from aiogram_dialog import DialogManager, StartMode

from fluent.runtime import FluentLocalization
from fluent.runtime.types import fluent_number

from tgbot.handlers.admin.states.menu import AdminMenuSG
from tgbot.keyboard.inline.user import film_kb
from tgbot.services.repository import Repo

router = Router(name=__name__)


@router.message(Command("admin"))
async def admin_start_handler(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminMenuSG.main, mode=StartMode.RESET_STACK)


@router.message(CommandStart(deep_link=True))
async def share_film(
    m: Message,
    command: CommandObject,
    l10n: FluentLocalization,
    repo: Repo,
    dialog_manager: DialogManager,
):
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username,
    )

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
                    rating=film.rating or "0.0",
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
async def start_handler(
    m: Message, l10n: FluentLocalization, repo: Repo, dialog_manager: DialogManager
):
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username,
    )
    await m.answer(l10n.format_value("user-start-text"))


@router.message(Command("yn"))
async def yn_handler(
    m: Message, l10n: FluentLocalization, dialog_manager: DialogManager
):
    messages = [
        l10n.format_value("user-no-message"),
        l10n.format_value("user-yes-message"),
    ]

    await m.answer(l10n.format_value(random.choice(messages)))


@router.message(Command("chance"))
async def chance_handler(
    m: Message, l10n: FluentLocalization, dialog_manager: DialogManager
):
    await m.answer(
        l10n.format_value("user-percent-message", dict(percent=random.randint(0, 100)))
    )
