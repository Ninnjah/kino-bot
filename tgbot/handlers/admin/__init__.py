from aiogram import Router

from tgbot.filters.role import RoleFilter
from tgbot.models.role import UserRole

from . import start
from . import admins
from . import users

__all__ = (
    "router",
)

router = Router(name=__name__)
router.message.filter(RoleFilter(UserRole.ADMIN))
router.callback_query.filter(RoleFilter(UserRole.ADMIN))

router.include_routers(
    start.router,
    admins.router,
    users.router,
)
