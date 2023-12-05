from aiogram import Router
from . import start
from . import films
from . import errors

__all__ = (
    "router",
)

router = Router(name=__name__)

router.include_routers(
    start.router,
    films.router,
    errors.router,
)
