import logging
from operator import itemgetter
from typing import Any

from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Multiselect, Cancel
from aiogram_dialog.widgets.text import Format
from tgbot.services.l10n_dialog import L10NFormat

from tgbot.handlers.admin.states.players import PlayerConfigSG
from tgbot.services.repository import Repo

router = Router(name=__name__)
logger = logging.getLogger(__name__)


async def start_config(start_data: Any, manager: DialogManager):
    repo = manager.middleware_data["repo"]
    players = await repo.list_players()

    widget: Multiselect = manager.find("players_ms")

    for player in players:
        await widget.set_checked(item_id=str(player.title), checked=player.is_active)


async def list_players(dialog_manager: DialogManager, repo: Repo, **kwargs):
    players = await repo.list_players()

    return {"players": [(i.title, i.is_active) for i in players] if players else []}


async def update_player_handlers(callback: CallbackQuery, select: Multiselect, manager: DialogManager, player_title: str):
    repo = manager.middleware_data["repo"]

    active = not select.is_checked(player_title)
    await repo.toggle_player(player_title, active)


players_dialog = Dialog(
    Window(
        L10NFormat("admin-players-list-text"),
        ScrollingGroup(
            Multiselect(
                Format("✅ {item[0]}"),
                Format("❌ {item[0]}"),
                id="players_ms",
                items="players",
                item_id_getter=itemgetter(0),
                on_click=update_player_handlers
            ),
            width=1,
            height=5,
            hide_on_single_page=True,
            id="scroll_with_pager",
        ),
        Cancel(text=L10NFormat("close-button-text")),
        getter=list_players,
        state=PlayerConfigSG.main,
    ),
    on_start=start_config
)

router.include_routers(
    players_dialog,
)
