import logging
from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

from tgbot.filters.text import TextFilter
from tgbot.handlers.admin.states.admins import AddAdminSG, DelAdminSG
from tgbot.keyboard.reply import cancel_kb
from tgbot.keyboard.reply.admin import main_kb
from tgbot.keyboard.inline import yesno_kb
from tgbot.services.repository import Repo
from tgbot.services.parts import split_message

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(TextFilter("admin-list-admin-button-text"))
async def list_handler(m: Message, l10n: FluentLocalization, repo: Repo):
    user_list = await repo.list_admins()

    if not user_list:
        await m.answer(l10n.format_value("admin-admins-list-handler-error-notfound"))
        return

    msg_text: str = ""
    for num, user in enumerate(user_list, start=1):
        msg_text += "{num}. <a href='tg://user?id={user_id}'><b>{user_id}</b></a> [{date}]\n".format(
            num=num, user_id=user.user_id, date=user.created_on
        )

    for message in split_message(msg_text):
        await m.answer(message)


@router.message(TextFilter("admin-add-admin-button-text"))
async def add_request(m: Message, l10n: FluentLocalization, state: FSMContext):
    await state.clear()
    await m.answer(
        l10n.format_value("admin-admins-add-request-text"),
        reply_markup=cancel_kb.get(l10n),
    )
    await state.set_state(AddAdminSG.user_id)


@router.message(StateFilter(AddAdminSG.user_id))
async def add_handler(
    m: Message, l10n: FluentLocalization, repo: Repo, state: FSMContext
):
    try:
        # If message is forwarded take user id from it
        if getattr(m, "forward_from", None):
            user_id = m.forward_from.id

        # Else get user id from message text
        else:
            user_id: int = int(m.text)

    except ValueError:
        await m.reply(
            l10n.format_value("error-user-id-is-invalid"),
            reply_markup=cancel_kb.get(l10n),
        )
        return

    else:
        # If message from group or channel
        if user_id < 0:
            await m.reply(
                l10n.format_value("error-is-not-user-id"),
                reply_markup=cancel_kb.get(l10n),
            )
            return

        # If user is not an admin
        elif not await repo.is_admin(user_id):
            await m.answer(
                l10n.format_value(
                    "admin-admins-add-handler-confirm", dict(user_id=user_id)
                ),
                reply_markup=yesno_kb.get(l10n, user_id),
            )
            await state.set_state(AddAdminSG.confirm)

        # If user is admin
        else:
            await m.reply(
                l10n.format_value("admin-admins-add-handler-error-already-admin"),
                reply_markup=cancel_kb.get(l10n),
            )


@router.callback_query(
    StateFilter(AddAdminSG.confirm), yesno_kb.YesNoCallback.filter(F.action == True)
)
async def add_conf(
    callback: CallbackQuery,
    callback_data: yesno_kb.YesNoCallback,
    l10n: FluentLocalization,
    state: FSMContext,
    repo: Repo,
):
    # Get user id from callback data
    user_id = int(callback_data.data)
    await repo.add_admin(user_id=user_id)
    logger.info(f"ADMIN {callback.from_user.id} ADD USER {user_id} TO ADMIN LIST")

    # Send success message
    await callback.message.answer(
        l10n.format_value("admin-admins-add-conf-success", dict(user_id=user_id)),
        reply_markup=main_kb.get(l10n),
    )
    await state.clear()


@router.callback_query(
    StateFilter(AddAdminSG.confirm), yesno_kb.YesNoCallback.filter(F.action == False)
)
async def add_reject(
    callback: CallbackQuery, l10n: FluentLocalization, state: FSMContext
):
    with suppress(TelegramForbiddenError, TelegramBadRequest):
        await callback.message.delete()

    await callback.message.answer(
        l10n.format_value("admin-admins-add-conf-reject"),
        reply_markup=main_kb.get(l10n),
    )
    await state.clear()


@router.message(TextFilter("admin-delete-admin-button-text"))
async def del_request(m: Message, l10n: FluentLocalization, state: FSMContext):
    await state.clear()
    await m.answer(
        l10n.format_value("admin-admins-del-request-text"),
        reply_markup=cancel_kb.get(l10n),
    )
    await state.set_state(DelAdminSG.user_id)


@router.message(StateFilter(DelAdminSG.user_id))
async def del_handler(
    m: Message, l10n: FluentLocalization, repo: Repo, state: FSMContext
):
    try:
        # If message is forwarded take user id from it
        if getattr(m, "forward_from", None):
            user_id = m.forward_from.id

        # Else get user id from message text
        else:
            user_id: int = int(m.text)

    except ValueError:
        await m.reply(
            l10n.format_value("error-user-id-is-invalid"),
            reply_markup=cancel_kb.get(l10n),
        )
        return

    else:
        # If message from group or channel
        if user_id < 0:
            await m.reply(
                l10n.format_value("error-is-not-user-id"),
                reply_markup=cancel_kb.get(l10n),
            )
            return

        # If user is not an admin
        elif await repo.is_admin(user_id):
            await m.answer(
                l10n.format_value(
                    "admin-admins-del-handler-confirm", dict(user_id=user_id)
                ),
                reply_markup=yesno_kb.get(l10n, user_id),
            )
            await state.set_state(DelAdminSG.confirm)

        # If user is admin
        else:
            await m.reply(
                l10n.format_value("admin-admins-del-handler-error-not-admin"),
                reply_markup=cancel_kb.get(l10n),
            )


@router.callback_query(
    StateFilter(DelAdminSG.confirm), yesno_kb.YesNoCallback.filter(F.action == True)
)
async def del_conf(
    callback: CallbackQuery,
    callback_data: yesno_kb.YesNoCallback,
    l10n: FluentLocalization,
    state: FSMContext,
    repo: Repo,
):
    # Get user id from callback data
    user_id = int(callback_data.data)
    await repo.del_admin(user_id=user_id)
    logger.info(f"ADMIN {callback.from_user.id} DEL USER {user_id} FROM ADMIN LIST")

    # Send success message
    await callback.message.answer(
        l10n.format_value("admin-admins-del-conf-success", dict(user_id=user_id)),
        reply_markup=main_kb.get(l10n),
    )
    await state.clear()


@router.callback_query(
    StateFilter(DelAdminSG.confirm), yesno_kb.YesNoCallback.filter(F.action == False)
)
async def del_reject(
    callback: CallbackQuery, l10n: FluentLocalization, state: FSMContext
):
    with suppress(TelegramForbiddenError, TelegramBadRequest):
        await callback.message.delete()

    await callback.message.answer(
        l10n.format_value("admin-admins-del-conf-reject"),
        reply_markup=main_kb.get(l10n),
    )
    await state.clear()
