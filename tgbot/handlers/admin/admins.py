import logging
from operator import itemgetter

from aiogram import Router
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Row,
    Button,
    ScrollingGroup,
    Select,
    Checkbox,
    ManagedCheckbox,
    Back,
)

from fluent.runtime.builtins import fluent_number

from tgbot.handlers.admin.states.admins import AdminSG, AddAdminSG, DelAdminSG
from tgbot.services.l10n_dialog import L10NFormat
from tgbot.services.repository import Repo

logger = logging.getLogger(__name__)
router = Router(name=__name__)


async def get_admin_id(dialog_manager: DialogManager, **kwargs):
    admin_id = dialog_manager.dialog_data.get("admin_id")
    return {"admin_id": str(admin_id)}


async def get_admin(dialog_manager: DialogManager, repo: Repo, **kwargs):
    admin_id = dialog_manager.dialog_data.get(
        "admin_id"
    ) or dialog_manager.start_data.get("admin_id")
    admin = await repo.get_admin(admin_id)

    sudo_checkbox = dialog_manager.find("admin_sudo_ch")
    if sudo_checkbox:
        await sudo_checkbox.set_checked(admin.sudo)

    return {
        "admin_id": str(admin.id),
        "sudo": admin.sudo,
        "created_on": admin.created_on.strftime("%Y.%m.%d %H:%M"),
        "updated_on": admin.updated_on.strftime("%Y.%m.%d %H:%M"),
    }


async def get_admins(dialog_manager: DialogManager, repo: Repo, **kwargs):
    admins = await repo.list_admins()
    return {
        "admins": [(admin.id, admin.id, "🔑 " if admin.sudo else "") for admin in admins]
    }


async def get_users(dialog_manager: DialogManager, repo: Repo, **kwargs):
    users = await repo.list_users()
    return {"users": [(user.id, user) for user in users]}


async def show_admin(
    callback: CallbackQuery, select: Select, manager: DialogManager, admin_id: str
):
    manager.dialog_data["admin_id"] = int(admin_id)
    await manager.next()


async def change_sudo_status(
    callback: CallbackQuery, checkbox: ManagedCheckbox, manager: DialogManager
):
    repo: Repo = manager.middleware_data["repo"]
    sudo = not checkbox.is_checked()
    admin_id = manager.dialog_data["admin_id"]

    await repo.set_admin_sudo(admin_id, sudo)


async def admin_add_start(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.start(AddAdminSG.user_id)


async def admin_add_user_id(
    m: Message, message_input: MessageInput, manager: DialogManager
):
    l10n = manager.middleware_data["l10n"]
    repo = manager.middleware_data["repo"]

    try:
        if getattr(m, "forward_from", None):
            user_id = m.forward_from.id
        else:
            user_id: int = int(m.text)

    except ValueError:
        await m.reply(l10n.format_value("admin-error-user-id-is-invalid"))
        return

    else:
        if user_id < 0:
            await m.reply(l10n.format_value("admin-error-is-not-user-id"))
            return

        elif not await repo.is_admin(user_id):
            manager.dialog_data["admin_id"] = user_id
            await manager.next()

        else:
            await m.reply(l10n.format_value("admin-error-already-admin"))


async def admin_add_user_id_select(
    callback: CallbackQuery, select: Select, manager: DialogManager, admin_id: str
):
    l10n = manager.middleware_data["l10n"]
    repo = manager.middleware_data["repo"]
    user_id = int(admin_id)

    if not await repo.is_admin(user_id):
        manager.dialog_data["admin_id"] = user_id
        await manager.next()
    else:
        await callback.answer(
            l10n.format_value("admin-error-already-admin"),
            show_alert=True,
        )


async def add_admin_sudo_handler(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    is_sudo = button.widget_id == "yes"
    manager.dialog_data["sudo"] = is_sudo
    await manager.next()


async def add_admin_accept_handler(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    repo = manager.middleware_data["repo"]

    await repo.add_admin(
        user_id=manager.dialog_data.get("admin_id"),
        sudo=manager.dialog_data.get("sudo"),
    )
    user_id = fluent_number(manager.dialog_data.get("admin_id"), useGrouping=False)
    logger.info(f"ADMIN {callback.from_user.id} ADD USER {user_id} TO ADMIN LIST")

    await manager.start(AdminSG.lst, mode=StartMode.RESET_STACK)


async def admin_del_start(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.start(
        DelAdminSG.confirm, data={"admin_id": manager.dialog_data["admin_id"]}
    )


async def admin_del(callback: CallbackQuery, button: Button, manager: DialogManager):
    repo: Repo = manager.middleware_data["repo"]
    admin_id = manager.start_data["admin_id"]

    await repo.del_admin(admin_id)
    await manager.start(AdminSG.lst, mode=StartMode.RESET_STACK)


admin_list_dialog = Dialog(
    Window(
        L10NFormat("admin-admins-list"),
        ScrollingGroup(
            Select(
                Format("{item[2]}{item[1]}"),
                id="admin_list",
                item_id_getter=itemgetter(0),
                items="admins",
                on_click=show_admin,
            ),
            id="admin_list_sg",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        Button(
            L10NFormat("admin-button-add-admin"),
            id="admin_add",
            on_click=admin_add_start,
        ),
        getter=get_admins,
        state=AdminSG.lst,
    ),
    Window(
        L10NFormat("admin-show-admin"),
        Checkbox(
            L10NFormat("admin-show-sudo"),
            L10NFormat("admin-show-sudo"),
            id="admin_sudo_ch",
            on_click=change_sudo_status,
        ),
        Button(
            L10NFormat("admin-button-del-admin"),
            id="admin_del",
            on_click=admin_del_start,
        ),
        Back(L10NFormat("admin-button-back")),
        getter=get_admin,
        state=AdminSG.profile,
    ),
)


admin_add_dialog = Dialog(
    Window(
        L10NFormat("admin-add-admin-request"),
        MessageInput(admin_add_user_id),
        ScrollingGroup(
            Select(
                Format("{item[1].id}"),
                id="user_list",
                item_id_getter=itemgetter(0),
                items="users",
                on_click=admin_add_user_id_select,
            ),
            id="admin_list_sg",
            width=1,
            height=10,
            hide_on_single_page=True,
        ),
        Cancel(text=L10NFormat("admin-button-cancel")),
        getter=get_users,
        state=AddAdminSG.user_id,
    ),
    Window(
        L10NFormat("admin-add-admin-sudo-request"),
        Row(
            Button(
                L10NFormat("admin-button-yes"),
                id="yes",
                on_click=add_admin_sudo_handler,
            ),
            Button(
                L10NFormat("admin-button-no"),
                id="no",
                on_click=add_admin_sudo_handler,
            ),
        ),
        Cancel(text=L10NFormat("admin-button-cancel")),
        getter=get_admin_id,
        state=AddAdminSG.sudo,
    ),
    Window(
        L10NFormat("admin-add-admin-confirm"),
        Row(
            Button(
                L10NFormat("admin-button-yes"),
                id="accept",
                on_click=add_admin_accept_handler,
            ),
            Cancel(text=L10NFormat("admin-button-no")),
        ),
        getter=get_admin_id,
        state=AddAdminSG.confirm,
    ),
)


admin_del_dialog = Dialog(
    Window(
        L10NFormat("admin-delete-text"),
        Row(
            Button(
                L10NFormat("admin-button-yes"),
                id="yes",
                on_click=admin_del,
            ),
            Cancel(L10NFormat("admin-button-cancel")),
        ),
        getter=get_admin,
        state=DelAdminSG.confirm,
    ),
)


router.include_routers(
    admin_list_dialog,
    admin_add_dialog,
    admin_del_dialog,
)
