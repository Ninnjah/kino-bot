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
        data: Dict[str, Any],
    ) -> Any:
        roles = []
        repo = data["repo"]

        if not getattr(event, "from_user", None):
            data["roles"] = None

        else:
            roles.append(UserRole.USER)
            admin = await repo.is_admin(event.from_user.id)

            is_sudo = any(
                (
                    event.from_user.id in self.admin_list,
                    admin.sudo if admin else False,
                )
            )
            is_admin = admin is not None

            if is_sudo:
                roles.append(UserRole.SUDO)
                roles.append(UserRole.ADMIN)
            elif is_admin:
                roles.append(UserRole.ADMIN)

        data["roles"] = roles

        result = await handler(event, data)

        del data["roles"]
        return result
