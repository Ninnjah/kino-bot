from aiogram import Router
from . import films
from . import errors

__all__ = ("router",)

router = Router(name=__name__)

router.include_routers(
    films.router,
    errors.router,
)
