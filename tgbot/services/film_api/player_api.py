import asyncio
import logging
from abc import abstractmethod
from typing import Optional, List

from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer
from httpx import AsyncClient, ConnectTimeout, ConnectError, ReadTimeout, Response

from tgbot.services.film_api.models import films
from tgbot.services.film_api.models.films import Source

logger = logging.getLogger(__name__)


class BasePlayer:
    TIMEOUT = 3
    def __init__(self):
        self.title = "base"
        self.base_url: str

    @staticmethod
    @cached(ttl=3600, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    @abstractmethod
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
                logger.warning(f"Exception {e} on {url}\nWaiting of {BasePlayer.TIMEOUT} seconds")
                await asyncio.sleep(BasePlayer.TIMEOUT)
                continue
    
    @staticmethod
    @abstractmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        ...
    
    @abstractmethod
    async def get_source(self, film: films.Film) -> Optional[Source]:
        ...
    
    @abstractmethod
    async def get_bunch_source(self, film_list: List[films.Film]) -> List[Source]:
        ...


class VoidboostPlayer(BasePlayer):
    def __init__(self):
        self.title = "voidboost"
        self.base_url = "https://voidboost.tv"
    
    @staticmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        ...
    
    async def get_source(self, film: films.Film) -> Optional[Source]:
        async with AsyncClient() as client:
            res = await self._request_get(client, f"{self.base_url}/embed/{film.film_id}")
            if res.status_code == 200:
                return Source(title=self.title, film_id=film.film_id, url=str(res.request.url))
    
    async def get_bunch_source(self, film_list: List[films.Film]) -> List[Source]:
        try:
            async with AsyncClient() as client:
                r = await asyncio.gather(
                    *[
                        self._request_get(client, f"{self.base_url}/embed/{film.film_id}")
                        for film in film_list
                    ]
                )
                return [
                    Source(title=self.title, film_id=x.request.url.path.split("/")[-1], url=str(x.request.url))
                    for x in r if x.status_code == 200 if x
                ]

        except (ReadTimeout, ConnectTimeout, ConnectError) as e:
            logger.warning(f"{e}\nWaiting of {BasePlayer.TIMEOUT} seconds", exc_info=True)
            await asyncio.sleep(BasePlayer.TIMEOUT)
            return await self.check_available(film_list)


class IframePlayer(BasePlayer):
    def __init__(self):
        self.title = "iframe"
        self.base_url = "https://iframe.video/api/v2"
    
    @staticmethod
    async def _parse_url(raw_data: dict) -> Optional[str]:
        try:
            return raw_data["results"][0]["path"]
        except (IndexError, TypeError):
            return
    
    @abstractmethod
    async def get_source(self, film: films.Film) -> Optional[Source]:
        async with AsyncClient() as client:
            res = await self._request_get(client, f"{self.base_url}/search", params={"kp": film.film_id})
            if res.status_code == 200:
                return Source(title=self.title, film_id=film.film_id, url=await self._parse_url(res.json()))
    
    async def get_bunch_source(self, film_list: List[films.Film]) -> List[Source]:
        try:
            async with AsyncClient() as client:
                r = await asyncio.gather(
                    *[
                        self._request_get(client, f"{self.base_url}/search", params={"kp": film.film_id})
                        for film in film_list
                    ]
                )
                
                return [
                    Source(title=self.title, film_id=x.request.url.params["kp"], url=await self._parse_url(x.json()))
                    for x in r if x.status_code == 200 if x and x.json()["results"]
                ]

        except (ReadTimeout, ConnectTimeout, ConnectError) as e:
            logger.warning(f"{e}\nWaiting of {BasePlayer.TIMEOUT} seconds", exc_info=True)
            await asyncio.sleep(BasePlayer.TIMEOUT)
            return await self.check_available(film_list)
