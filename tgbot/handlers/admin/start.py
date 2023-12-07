from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode

from fluent.runtime import FluentLocalization

from tgbot.handlers.admin.states.players import PlayerConfigSG
from tgbot.keyboard.reply.admin import main_kb
from tgbot.filters.text import TextFilter

router = Router(name=__name__)


@router.message(TextFilter("cancel-button-text"))
@router.message(Command("admin"))
async def start_handler(m: Message, l10n: FluentLocalization, state: FSMContext):
    await state.clear()
    await m.answer(l10n.format_value("admin-start-text"), reply_markup=main_kb.get(l10n))


@router.message(TextFilter("admin-list-players-button-text"))
async def list_handler(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(PlayerConfigSG.main, mode=StartMode.RESET_STACK)
    return
