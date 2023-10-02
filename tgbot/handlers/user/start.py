from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.services.repository import Repo

router = Router(name=__name__)


@router.message(Command("start"))
async def start_handler(m: Message, l10n: FluentLocalization, repo: Repo):
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username,
    )
    await m.answer(l10n.format_value("user-start-text"))
