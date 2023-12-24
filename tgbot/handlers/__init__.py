from aiogram import Router
from . import commands
from . import admin
from . import user

__all__ = ("router",)

main_router = Router(name=__name__)

main_router.include_routers(
    commands.router,
    admin.router,
    user.router,
)
