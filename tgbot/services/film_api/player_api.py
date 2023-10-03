import asyncio
import re
import json
from typing import Optional, List

from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer
from httpx import AsyncClient

from tgbot.services.film_api.models.films import Film
from tgbot.services.film_api.models.player import Season, Episode, Source


class PlayerAPI:
    def __init__(self, token: str):
        self.token = token  # eedefb541aeba871dcfc756e6b31c02e

        self._base_url = f"https://api.bhcesh.me"
        self._franchise_details = f"{self._base_url}/franchise/details"

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
                    Season(
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
    async def get_film_data(self, kinopoisk_id: int) -> Optional[str]:
        params = {
            "token": self.token,
            "kinopoisk_id": kinopoisk_id
        }

        async with AsyncClient() as client:
            res = await client.get(self._franchise_details, params=params)
            if res.status_code == 200:
                return await self._parse_iframe_url(res.json())

    @cached(ttl=30, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def get_film_source(self, kinopoisk_id: int) -> Optional[Source]:
        link = await self.get_film_data(kinopoisk_id)
        if not link:
            return

        async with AsyncClient() as client:
            res = await client.get(link)
            return await self._parse_source(kinopoisk_id, res.text)

    @cached(ttl=3600, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def check_available(self, films: List[Film]) -> List[Source]:
        async with AsyncClient() as client:
            r = await asyncio.gather(
                *[
                    client.get(
                        self._franchise_details,
                        params={
                            "token": self.token,
                            "kinopoisk_id": film.film_id
                        }
                    )
                    for film in films
                ]
            )
            links = [
                (x.request.url.params["kinopoisk_id"], await self._parse_iframe_url(x.json()))
                for x in r if x.status_code == 200
            ]

            r = await asyncio.gather(
                *[
                    client.get(link[1], params={"kinopoisk_id": link[0]})
                    for link in links
                ]
            )
            sources = [
                await self._parse_source(x.request.url.params["kinopoisk_id"], x.text)
                for x in r if x.status_code == 200
            ]

        return sources
