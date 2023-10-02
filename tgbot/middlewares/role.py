from typing import Callable, Dict, Any, Awaitable, List

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tgbot.models.role import UserRole


class RoleMiddleware(BaseMiddleware):
    def __init__(self, admin_list: List[int]):
        self.admin_list = admin_list

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not getattr(event, "from_user", None):
            data["role"] = None
        elif any((
            event.from_user.id in self.admin_list,
            await data["repo"].is_admin(event.from_user.id)
        )):
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

        result = await handler(event, data)

        del data["role"]
        return result
