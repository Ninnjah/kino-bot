from aiogram import Router
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.filters.text import TextFilter
from tgbot.services.repository import Repo
from tgbot.services.parts import split_message

router = Router(name=__name__)


@router.message(TextFilter("admin-list-user-button-text"))
async def list_users(m: Message, l10n: FluentLocalization, repo: Repo):
    user_list = await repo.list_users()

    if not user_list:
        await m.answer(l10n.format_value("admin-list-user-error-notfound"))
        return

    msg_text: str = ""
    for num, user in enumerate(user_list, start=1):
        msg_text += "{num}. <a href='tg://user?id={user_id}'><b>{user_id}</b></a> [{date}]\n".format(
            num=num,
            user_id=user.user_id,
            date=user.created_on
        )

    for message in split_message(msg_text):
        await m.answer(message)
