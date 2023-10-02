import re
import json
from typing import Optional, Union, List

from aiocache import cached
from aiocache.serializers import PickleSerializer
from httpx import AsyncClient

from tgbot.services.film_api.models.player import Season, Episode, Source


class PlayerAPI:
    def __init__(self, token: str):
        self.token = token  # eedefb541aeba871dcfc756e6b31c02e

        self._base_url = f"https://api.bhcesh.me"
        self._franchise_details = f"{self._base_url}/franchise/details"

    @cached(ttl=10, serializer=PickleSerializer(), namespace="cache")
    async def get_film_data(self, kinopoisk_id: int) -> Optional[str]:
        params = {
            "token": self.token,
            "kinopoisk_id": kinopoisk_id
        }

        async with AsyncClient() as client:
            res = await client.get(self._franchise_details, params=params)
            if res.status_code == 200:
                data = res.json()
                return data.get("iframe_url")

    @cached(ttl=10, serializer=PickleSerializer(), namespace="cache")
    async def get_film_source(self, kinopoisk_id: int) -> Optional[Union[List[Season], Source]]:
        link = await self.get_film_data(kinopoisk_id)

        async with AsyncClient() as client:
            res = await client.get(link)
            player_info = re.search(re.compile(r"makePlayer\(({[^;]+})\)"), res.text)
            player_info = player_info.group(1)

            raw_seasons = re.search(re.compile(r"seasons:(\[.+\])"), player_info)
            if raw_seasons:
                data = json.loads(raw_seasons.group(1))
                return [
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

            else:
                raw_url = re.search(re.compile(r"hls:.*\"(.+)\""), player_info)
                if raw_url:
                    data = raw_url.group(1)
                    return Source(data)
