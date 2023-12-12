import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from aiogram_dialog import setup_dialogs

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool import AsyncAdaptedQueuePool

import redis.asyncio as redis

from tgbot.config_reader import config
from tgbot.fluent_loader import get_fluent_localization
from tgbot.handlers import admin, user
from tgbot.middlewares.media_group import AlbumMiddleware
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.services.film_api import KinopoiskAPI, players
from tgbot.services.repository import Repo

logger = logging.getLogger(__name__)


async def create_pool(db_url: str, echo: bool = False) -> AsyncEngine:
    engine = create_async_engine(
        db_url, poolclass=AsyncAdaptedQueuePool, pool_size=5, max_overflow=10, echo=echo
    )

    async with engine.begin() as conn:
        repo = Repo(conn)
        await repo.init_players([x.title for x in players])

    return engine


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    if config.use_redis:
        storage = RedisStorage(
            redis.Redis(),
            key_builder=DefaultKeyBuilder(
                prefix=config.redis_prefix, with_destiny=True
            ),
        )
    else:
        storage = MemoryStorage()

    pool = await create_pool(config.database_url.unicode_string())
    bot = Bot(
        config.bot_token.get_secret_value(),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    dp = Dispatcher(storage=storage)

    dp["admin_list"] = config.admin_list
    dp["l10n"] = get_fluent_localization()
    dp["kinopoisk"] = KinopoiskAPI(config.kinopoisk_token.get_secret_value())

    dp.message.middleware(AlbumMiddleware())

    dp.message.outer_middleware(DbMiddleware(pool))
    dp.callback_query.outer_middleware(DbMiddleware(pool))
    dp.message.outer_middleware(RoleMiddleware(config.admin_list))
    dp.callback_query.outer_middleware(RoleMiddleware(config.admin_list))

    dp.include_routers(
        admin.router,
        user.router,
    )

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    # start
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
