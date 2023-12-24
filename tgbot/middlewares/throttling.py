import time
from asyncio import sleep
from typing import Callable, Awaitable, Any, Dict, Optional, MutableMapping

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    RATE_LIMIT = 0.7

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache: MutableMapping[int, None] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if all(
            (
                user is not None,
                isinstance(event, Message) and event.media_group_id is None,
            )
        ):
            if user.id in self.cache:
                return None

            self.cache[user.id] = None

        return await handler(event, data)


class InlineQueryThrottlingMiddleware(BaseMiddleware):
    LATENCY = 5
    RATE_LIMIT = 6

    def __init__(
        self, latency: float = LATENCY, rate_limit: float = RATE_LIMIT
    ) -> None:
        self.latency = latency
        self.cache: MutableMapping[int, str] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)
        key = user.id
        self.cache[key] = time.time()

        await sleep(self.latency)
        if time.time() - self.cache[key] < self.latency:
            return None

        return await handler(event, data)
