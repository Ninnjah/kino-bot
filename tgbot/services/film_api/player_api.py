import asyncio
import json
import re
import logging
from typing import Optional, List, Union

from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer
from httpx import AsyncClient, ConnectTimeout, ConnectError, ReadTimeout, Response

from tgbot.services.film_api.models import films
from tgbot.services.film_api.models.player import Season, Episode, Source, Film, Serial, SourceSeason

logger = logging.getLogger(__name__)
TIMEOUT = 3


class PlayerAPI:
    def __init__(self, token: str):
        self.token = token  # eedefb541aeba871dcfc756e6b31c02e

        self._base_url = f"https://api.bhcesh.me"
        self._franchise_details = f"{self._base_url}/franchise/details"

    @staticmethod
    @cached(ttl=3600, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def _request_get(
            client: AsyncClient, url: str, params: Optional[dict] = None, timeout: int = TIMEOUT, attempts: int = 5
    ) -> Optional[Response]:
        for _ in range(attempts):
            try:
                return await client.get(url, params=params)
            except (ReadTimeout, ConnectTimeout, ConnectError) as e:
                logger.warning(f"Exception {e} on {url}\nWaiting of {TIMEOUT} seconds", exc_info=True)
                await asyncio.sleep(timeout)
                continue

    @staticmethod
    async def _parse_iframe_url(raw_data: dict) -> Optional[str]:
        return raw_data.get("iframe_url")

    @staticmethod
    async def _parse_source(kinopoisk_id: int, raw_data: str) -> Optional[Source]:
        player_info = re.search(re.compile(r"makePlayer\(({[^;]+})\)"), raw_data)
        player_info = player_info.group(1)

        raw_seasons = re.search(re.compile(r"seasons:(\[.+\])"), player_info)
        if raw_seasons:
            data = json.loads(raw_seasons.group(1))
            return Source(
                film_id=kinopoisk_id,
                seasons=[
                    SourceSeason(
                        number=season["season"],
                        episodes=[
                            Episode(
                                number=episode["episode"],
                                url=episode["hls"],
                            )
                            for episode in season["episodes"]
                        ],
                    )
                    for season in data
                ]
            )

        else:
            raw_url = re.search(re.compile(r"hls:.*\"(.+)\""), player_info)
            if raw_url:
                data = raw_url.group(1)
                return Source(film_id=kinopoisk_id, url=data)

    @cached(ttl=30, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def get_film_url(self, kinopoisk_id: int) -> Optional[str]:
        params = {
            "token": self.token,
            "kinopoisk_id": kinopoisk_id
        }

        async with AsyncClient() as client:
            res = await self._request_get(client, self._franchise_details, params=params)
            if res.status_code == 200:
                return await self._parse_iframe_url(res.json())

    @cached(ttl=30, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def get_film_source(self, kinopoisk_id: int) -> Optional[Source]:
        link = await self.get_film_url(kinopoisk_id)
        if not link:
            return

        async with AsyncClient() as client:
            res = await self._request_get(client, link)
            return await self._parse_source(kinopoisk_id, res.text)

    async def get_film_data(self, kinopoisk_id: int) -> Optional[Union[Film, Serial]]:
        params = {
            "token": self.token,
            "kinopoisk_id": kinopoisk_id
        }

        async with AsyncClient() as client:
            res = await self._request_get(client, self._franchise_details, params=params)
            if res.status_code == 200:
                raw_data = res.json()
                if not raw_data.get("type"):
                    return

                elif raw_data.get("type") in {"series", "cartoon-series"}:
                    return Serial(
                        film_id=raw_data.get("kinopoisk_id"),
                        name_ru=raw_data.get("name"),
                        name_en=raw_data.get("name_eng"),
                        year=raw_data.get("year"),
                        description=raw_data.get("description"),
                        film_length=raw_data.get("time"),
                        countries=[x for x in raw_data.get("country").values()],
                        genres=[x for x in raw_data.get("genre").values()],
                        rating=raw_data.get("kinopoisk"),
                        poster_url=raw_data.get("poster"),
                        url=raw_data.get("iframe_url"),
                        seasons=[
                            Season(
                                number=season.get("season"),
                                url=season.get("iframe_url"),
                                episodes=[
                                    Episode(
                                        number=episode.get("episode"),
                                        url=episode.get("iframe_url"),
                                    )
                                    for episode in season.get("episodes")
                                ],
                            ) for season in raw_data.get("seasons")
                        ]
                    )

                else:
                    return Film(
                        film_id=raw_data.get("kinopoisk_id"),
                        name_ru=raw_data.get("name"),
                        name_en=raw_data.get("name_eng"),
                        year=raw_data.get("year"),
                        description=raw_data.get("description"),
                        film_length=raw_data.get("time"),
                        countries=[x for x in raw_data.get("country").values()],
                        genres=[x for x in raw_data.get("genre").values()],
                        rating=raw_data.get("kinopoisk"),
                        poster_url=raw_data.get("poster"),
                        url=raw_data.get("iframe_url"),
                    )

    @cached(ttl=3600, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def check_available(self, film_list: List[films.Film]) -> List[Source]:
        try:
            async with AsyncClient() as client:
                r = await asyncio.gather(
                    *[
                        self._request_get(
                            client,
                            self._franchise_details,
                            params={
                                "token": self.token,
                                "kinopoisk_id": film.film_id
                            }
                        )
                        for film in film_list
                    ]
                )
                links = [
                    (x.request.url.params["kinopoisk_id"], await self._parse_iframe_url(x.json()))
                    for x in r if x.status_code == 200
                ]

                r = await asyncio.gather(
                    *[
                        self._request_get(client, link[1], params={"kinopoisk_id": link[0]})
                        for link in links if link[1]
                    ]
                )
                sources = [
                    await self._parse_source(x.request.url.params["kinopoisk_id"], x.text)
                    for x in r if x.status_code == 200
                ]

        except (ReadTimeout, ConnectTimeout, ConnectError) as e:
            logger.warning(f"{e}\nWaiting of {TIMEOUT} seconds", exc_info=True)
            await asyncio.sleep(TIMEOUT)
            return await self.check_available(film_list)

        return sources
