import asyncio
import logging
from contextlib import suppress
from typing import Sequence

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import CallbackQuery, Message, ContentType

from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.manager.bg_manager import BgManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Back,
    Next,
    Row,
    StubScroll,
    Group,
    NumberedPager,
    SwitchTo,
    Button,
)
from fluent.runtime import FluentLocalization

from tgbot.handlers.admin.states.messages import MessageSG
from tgbot.models.album import Album, INPUT_TYPES
from tgbot.services.l10n_dialog import L10NFormat
from tgbot.services.repository import Repo

logger = logging.getLogger(__name__)
router = Router(name=__name__)
FINISHED_KEY = "finished"
CANCEL_EDIT = SwitchTo(
    L10NFormat("admin-button-cancel-edit"),
    when=F["dialog_data"][FINISHED_KEY],
    id="cnl_edt",
    state=MessageSG.preview,
)


async def next_or_end(event, widget, dialog_manager: DialogManager, *_):
    if dialog_manager.dialog_data.get(FINISHED_KEY):
        await dialog_manager.switch_to(MessageSG.preview)
    else:
        await dialog_manager.next()


async def load_message(dialog_manager: DialogManager, **kwargs):
    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    media_list = dialog_manager.dialog_data.get("media", [])
    text = dialog_manager.dialog_data.get("text")
    if not media_list:
        return {
            "media_count": len(media_list),
            "media_number": media_number + 1,
            "media": None,
            "text": text,
        }

    media = media_list[media_number]
    return {
        "media_count": len(media_list),
        "media_number": media_number + 1,
        "media": MediaAttachment(type=media[0], file_id=MediaId(media[1])),
        "text": text,
    }


async def result_getter(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data[FINISHED_KEY] = True
    return await load_message(dialog_manager)


async def post_handler(m: Message, input: MessageInput, manager: DialogManager):
    manager.dialog_data["text"] = m.html_text
    await manager.next()


async def post_media_handler(m: Message, input: MessageInput, manager: DialogManager):
    album: Album = manager.middleware_data["album"]
    manager.dialog_data["media"] = [
        (media.type, media.media) for media in album.as_media_group
    ]
    await manager.next()


async def send_preview(callback: CallbackQuery, button: Button, manager: DialogManager):
    media_list = manager.dialog_data.get("media", [])
    text = manager.dialog_data.get("text")

    if media_list:
        await callback.message.answer_media_group(
            [
                INPUT_TYPES[media[0]](
                    type=media[0],
                    media=media[1],
                    caption=text if i == 0 else None,
                )
                for i, media in enumerate(media_list)
            ]
        )
    else:
        await callback.message.answer(text)


async def send_message(callback: CallbackQuery, button: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data["repo"]
    l10n: FluentLocalization = manager.middleware_data["l10n"]
    bot = callback.bot

    user_list = await repo.list_users()
    media_list = manager.dialog_data.get("media", [])
    text = manager.dialog_data.get("text")

    for user in user_list:
        if media_list:
            await bot.send_media_group(
                chat_id=user.id,
                media=[
                    INPUT_TYPES[media[0]](
                        type=media[0],
                        media=media[1],
                        caption=text if i == 0 else None,
                    )
                    for i, media in enumerate(media_list)
                ],
            )
        else:
            await bot.send_message(chat_id=user.id, text=text)

    await callback.answer(l10n.format_value("admin-messages-sent"), show_alert=True)
    await manager.done()


post_dialog = Dialog(
    Window(
        L10NFormat("admin-message-media-request-text"),
        MessageInput(
            post_media_handler,
            content_types=[ContentType.PHOTO, ContentType.VIDEO],
        ),
        SwitchTo(
            L10NFormat("admin-button-skip"), id="media_skip", state=MessageSG.text
        ),
        CANCEL_EDIT,
        Cancel(L10NFormat("admin-button-cancel")),
        state=MessageSG.main,
    ),
    Window(
        L10NFormat("admin-message-media-preview-text"),
        DynamicMedia(selector="media"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=8,
        ),
        MessageInput(
            content_types=[ContentType.PHOTO, ContentType.VIDEO],
            func=post_media_handler,
        ),
        Row(
            Back(L10NFormat("admin-button-send-again")),
            Next(L10NFormat("admin-button-next")),
        ),
        CANCEL_EDIT,
        Cancel(L10NFormat("admin-button-cancel")),
        state=MessageSG.media,
        getter=load_message,
    ),
    Window(
        L10NFormat("admin-message-request-text"),
        MessageInput(
            post_handler,
            content_types=[ContentType.TEXT],
        ),
        CANCEL_EDIT,
        Cancel(L10NFormat("admin-button-cancel")),
        state=MessageSG.text,
    ),
    Window(
        L10NFormat("admin-message-preview-text"),
        DynamicMedia(selector="media"),
        StubScroll(id="pages", pages="media_count"),
        Group(NumberedPager(scroll="pages", when=F["pages"] > 1), width=8),
        MessageInput(
            content_types=[ContentType.PHOTO, ContentType.VIDEO],
            func=post_media_handler,
        ),
        SwitchTo(
            L10NFormat("admin-message-edit-media"),
            state=MessageSG.media,
            id="to_media",
        ),
        SwitchTo(
            L10NFormat("admin-message-edit-text"),
            state=MessageSG.text,
            id="to_text",
        ),
        Button(
            L10NFormat("admin-button-send-preview"),
            id="message_preview",
            on_click=send_preview,
        ),
        Button(
            L10NFormat("admin-button-send"),
            id="message_send",
            # on_click=send_message,
        ),
        Cancel(L10NFormat("admin-button-cancel")),
        state=MessageSG.preview,
        getter=result_getter,
    ),
)


router.include_routers(
    post_dialog,
)
