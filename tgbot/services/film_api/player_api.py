import asyncio
import logging
from abc import abstractmethod
from typing import Optional, List

from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer
from httpx import AsyncClient, ConnectTimeout, ConnectError, ReadTimeout, Response

from tgbot.services.film_api.models import Source, Film

logger = logging.getLogger(__name__)


def cache_key_builder(func, *args, **kwargs):
    ordered_kwargs = sorted(kwargs.items())
    return (func.__module__ or "") + func.__name__ + str(args[1:]) + str(ordered_kwargs)


class BasePlayer:
    TIMEOUT = 3

    def __init__(self):
        self.title = "base"
        self.base_url: str

    @staticmethod
    @cached(
        ttl=60,
        key_builder=cache_key_builder,
        cache=RedisCache,
        serializer=PickleSerializer(),
        namespace="cache",
    )
    async def _request_get(
        client: AsyncClient, url: str, params: Optional[dict] = None, attempts: int = 5
    ) -> Optional[Response]:
        for _ in range(attempts):
            try:
                result = await client.get(url, params=params)
                if result.status_code == 200:
                    return result

                elif result.status_code == 429:
                    await asyncio.sleep(BasePlayer.TIMEOUT)
                    continue

                else:
                    return result

            except (ReadTimeout, ConnectTimeout, ConnectError) as e:
                logger.warning(
                    f"Exception {e} on {url}\nWaiting of {BasePlayer.TIMEOUT} seconds"
                )
                await asyncio.sleep(BasePlayer.TIMEOUT)
                continue

    @staticmethod
    @abstractmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        ...

    @abstractmethod
    async def _get_source(
        self, client: AsyncClient, url: str, film: Film
    ) -> Optional[Source]:
        ...

    @abstractmethod
    async def get_source(self, film: Film) -> Optional[Source]:
        ...

    @abstractmethod
    async def get_bunch_source(self, film_list: List[Film]) -> List[Source]:
        ...


class VoidboostPlayer(BasePlayer):
    def __init__(self):
        self.title = "voidboost"
        self.base_url = "https://voidboost.tv"

    @staticmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        ...

    async def _get_source(
        self, client: AsyncClient, url: str, film: Film
    ) -> Optional[Source]:
        res = await self._request_get(client, url)
        if res.status_code == 200:
            return Source(
                title=self.title, film_id=film.film_id, url=str(res.request.url)
            )

    async def get_source(self, film: Film) -> Optional[Source]:
        async with AsyncClient() as client:
            res = await self._request_get(
                client, f"{self.base_url}/embed/{film.film_id}"
            )
            if res.status_code == 200:
                return Source(
                    title=self.title, film_id=film.film_id, url=str(res.request.url)
                )

    async def get_bunch_source(self, film_list: List[Film]) -> List[Source]:
        async with AsyncClient() as client:
            res = await asyncio.gather(
                *[
                    self._get_source(
                        client, url=f"{self.base_url}/embed/{film.film_id}", film=film
                    )
                    for film in film_list
                ]
            )
            return [x for x in res if x]


class IframePlayer(BasePlayer):
    def __init__(self):
        self.title = "iframe"
        self.base_url = "https://iframe.video/api/v2/search"

    @staticmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        try:
            return raw_data["results"][0]["path"]
        except (IndexError, TypeError):
            logger.error(f"URL parsing error - {raw_data}")
            return

    async def _get_source(
        self, client: AsyncClient, url: str, film: Film
    ) -> Optional[Source]:
        res = await self._request_get(client, url, params={"kp": film.film_id})
        if res.status_code == 200:
            data = res.json()
            source_url = await self._parse_url(data)
            if not source_url:
                return

            return Source(
                title=self.title,
                film_id=film.film_id,
                url=source_url,
            )

    async def get_source(self, film: Film) -> Optional[Source]:
        async with AsyncClient() as client:
            return await self._get_source(
                client, url=f"{self.base_url}/search", film=film
            )

    async def get_bunch_source(self, film_list: List[Film]) -> List[Source]:
        async with AsyncClient() as client:
            res = await asyncio.gather(
                *[
                    self._get_source(client, url=f"{self.base_url}/search", film=film)
                    for film in film_list
                ]
            )
            return [x for x in res if x]


class AllohaPlayer(BasePlayer):
    def __init__(self):
        self.title = "alloha"
        self.token = "04941a9a3ca3ac16e2b4327347bbc1"
        self.base_url = "https://api.alloha.tv"

    @staticmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        try:
            return raw_data["data"]["iframe"]
        except (IndexError, TypeError):
            logger.error(f"URL parsing error - {raw_data}")
            return

    async def _get_source(
        self, client: AsyncClient, url: str, film: Film
    ) -> Optional[Source]:
        res = await self._request_get(
            client, url, params={"token": self.token, "kp": film.film_id}
        )
        if res.status_code == 200:
            data = res.json()
            if data["status"] != "success":
                return
            source_url = await self._parse_url(data)
            if not source_url:
                return

            return Source(
                title=self.title,
                film_id=film.film_id,
                url=source_url,
            )

    async def get_source(self, film: Film) -> Optional[Source]:
        async with AsyncClient() as client:
            return await self._get_source(client, url=self.base_url, film=film)

    async def get_bunch_source(self, film_list: List[Film]) -> List[Source]:
        async with AsyncClient() as client:
            res = await asyncio.gather(
                *[
                    self._get_source(client, url=self.base_url, film=film)
                    for film in film_list
                ]
            )
            return [x for x in res if x]


class BhceshPlayer(BasePlayer):
    def __init__(self):
        self.title = "bhcesh"
        self.token = "eedefb541aeba871dcfc756e6b31c02e"
        self.base_url = "https://api.bhcesh.me/franchise/details"

    @staticmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        try:
            return raw_data["iframe_url"]
        except (IndexError, TypeError):
            logger.error(f"URL parsing error - {raw_data}")
            return

    async def _get_source(
        self, client: AsyncClient, url: str, film: Film
    ) -> Optional[Source]:
        res = await self._request_get(
            client, url, params={"token": self.token, "kinopoisk_id": film.film_id}
        )
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == 404:
                return
            source_url = await self._parse_url(data)
            if not source_url:
                return

            return Source(
                title=self.title,
                film_id=film.film_id,
                url=source_url,
            )

    async def get_source(self, film: Film) -> Optional[Source]:
        async with AsyncClient() as client:
            return await self._get_source(client, url=self.base_url, film=film)

    async def get_bunch_source(self, film_list: List[Film]) -> List[Source]:
        async with AsyncClient() as client:
            res = await asyncio.gather(
                *[
                    self._get_source(client, url=self.base_url, film=film)
                    for film in film_list
                ]
            )
            return [x for x in res if x]


class CollapsPlayer(BasePlayer):
    def __init__(self):
        self.title = "collaps"
        self.token = "eedefb541aeba871dcfc756e6b31c02e"
        self.base_url = "https://apicollaps.cc/list"

    @staticmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        try:
            return raw_data["results"][0]["iframe_url"]
        except (IndexError, TypeError):
            logger.error(f"URL parsing error - {raw_data}")
            return

    async def _get_source(
        self, client: AsyncClient, url: str, film: Film
    ) -> Optional[Source]:
        res = await self._request_get(
            client, url, params={"token": self.token, "kinopoisk_id": film.film_id}
        )
        if res.status_code == 200:
            data = res.json()
            if data["total"] == 0:
                return
            source_url = await self._parse_url(data)
            if not source_url:
                return

            return Source(
                title=self.title,
                film_id=film.film_id,
                url=source_url,
            )

    async def get_source(self, film: Film) -> Optional[Source]:
        async with AsyncClient() as client:
            return await self._get_source(client, url=self.base_url, film=film)

    async def get_bunch_source(self, film_list: List[Film]) -> List[Source]:
        async with AsyncClient() as client:
            res = await asyncio.gather(
                *[
                    self._get_source(client, url=self.base_url, film=film)
                    for film in film_list
                ]
            )
            return [x for x in res if x]
