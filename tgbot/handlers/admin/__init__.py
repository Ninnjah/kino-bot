from aiogram import Router, F
from aiogram.enums.chat_type import ChatType

from tgbot.filters.role import IsAdminFilter

from . import start
from . import admins
from . import users
from . import players

__all__ = ("router",)

router = Router(name=__name__)
router.message.filter(IsAdminFilter(), F.chat.type.in_({ChatType.PRIVATE}))
router.callback_query.filter(
    IsAdminFilter(),
    F.message.chat.type.in_({ChatType.PRIVATE}),
)

router.include_routers(
    start.router,
    admins.router,
    users.router,
    players.router,
)
