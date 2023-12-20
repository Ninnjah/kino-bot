from typing import Sequence

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode

from fluent.runtime import FluentLocalization

from tgbot.handlers.admin.states.admins import AdminSG
from tgbot.handlers.admin.states.users import UserSG
from tgbot.handlers.admin.states.players import PlayerConfigSG
from tgbot.keyboard.reply.admin import main_kb
from tgbot.filters.text import TextFilter
from tgbot.filters.role import IsAdminFilter, IsSudoFilter
from tgbot.models.role import UserRole
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


@router.message(Command("admin"))
async def admin_handler(
    m: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    dialog_manager: DialogManager,
    roles: Sequence[UserRole],
):
    await state.clear()
    await m.answer(
        l10n.format_value("admin-start-text"), reply_markup=main_kb.get(l10n, roles)
    )


@router.message(TextFilter("admin-button-list-admins"), IsSudoFilter())
async def list_admins(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminSG.lst, mode=StartMode.RESET_STACK)


@router.message(TextFilter("admin-button-list-users"), IsAdminFilter())
async def list_users(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserSG.lst, mode=StartMode.RESET_STACK)


@router.message(TextFilter("admin-button-list-players"))
async def list_handler(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(PlayerConfigSG.main, mode=StartMode.RESET_STACK)
