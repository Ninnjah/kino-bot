from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from tgbot.services.repository import Repo


class DbMiddleware(BaseMiddleware):
    def __init__(self, pool: AsyncEngine):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with self.pool.connect() as db:
            repo = Repo(db)
            data["repo"] = repo

            result = await handler(event, data)

            del data["repo"]
            return result
