import asyncio
import logging
from typing import Any, Optional

from httpx import AsyncClient, ConnectTimeout, ConnectError, ReadTimeout, Response

logger = logging.getLogger("kinopoisk_api.client.session.httpx")


class HttpxSession(AsyncClient):
    TIMEOUT = 3
    ATTEMPTS = 5

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    async def _request_get(
        self, url: str, params: Optional[dict] = None
    ) -> Optional[Response]:
        for _ in range(HttpxSession.ATTEMPTS):
            try:
                result = await self.get(url, params=params)
                if result.status_code == 200:
                    return result

                elif result.status_code == 429:
                    await asyncio.sleep(HttpxSession.TIMEOUT)
                    continue

                else:
                    return result

            except (ReadTimeout, ConnectTimeout, ConnectError) as e:
                logger.warning(
                    f"Exception {e} on {url}\nWaiting of {HttpxSession.TIMEOUT} seconds"
                )
                await asyncio.sleep(HttpxSession.TIMEOUT)
                continue
