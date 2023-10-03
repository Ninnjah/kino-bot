from datetime import datetime
from typing import Optional

from aiocache import cached, RedisCache
from aiocache.serializers import PickleSerializer
from httpx import AsyncClient

from tgbot.services.film_api.models.films import Film, FilmType, Search, DetailFilm, Season, Episode


class KinopoiskAPI:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "X-API-KEY": self.token
        }

        self.api_version = "v2.1"
        self._base_url = f"https://kinopoiskapiunofficial.tech/api/{self.api_version}"
        self._films = f"{self._base_url}/films"
        self._films_search_by_keyword = f"{self._films}/search-by-keyword"

    @staticmethod
    def _parse_film(raw_film: dict) -> Film:
        return Film(
            film_id=raw_film.get("filmId"),
            name_ru=raw_film.get("nameRu"),
            name_en=raw_film.get("nameEn"),
            type=FilmType(raw_film["type"]) if raw_film["type"] else None,
            year=raw_film.get("year"),
            description=raw_film.get("description"),
            film_length=raw_film.get("filmLength"),
            countries=[country["country"] for country in raw_film.get("countries", [])],
            genres=[genre["genre"] for genre in raw_film.get("genres", [])],
            rating=raw_film.get("rating"),
            rating_vote_count=raw_film.get("ratingVoteCount"),
            poster_url=raw_film.get("posterUrl"),
            poster_url_preview=raw_film.get("posterUrlPreview"),
        )

    @staticmethod
    def _parse_detailed_film(raw_film: dict) -> DetailFilm:
        return DetailFilm(
            film_id=raw_film.get("filmId"),
            name_ru=raw_film.get("nameRu"),
            name_en=raw_film.get("nameEn"),
            type=FilmType(raw_film["type"]) if raw_film["type"] else None,
            year=raw_film.get("year"),
            description=raw_film.get("description"),
            film_length=raw_film.get("filmLength"),
            countries=[country["country"] for country in raw_film.get("countries", [])],
            genres=[genre["genre"] for genre in raw_film.get("genres", [])],
            rating=raw_film.get("rating"),
            rating_vote_count=raw_film.get("ratingVoteCount"),
            poster_url=raw_film.get("posterUrl"),
            poster_url_preview=raw_film.get("posterUrlPreview"),
            distributor_release=raw_film.get("distributor_release"),
            distributors=raw_film.get("distributors"),
            facts=raw_film.get("facts"),
            premiere_bluray=raw_film.get("premiere_bluray"),
            premiere_digital=raw_film.get("premiere_digital"),
            premiere_dvd=raw_film.get("premiere_dvd"),
            premiere_ru=raw_film.get("premiere_ru"),
            premiere_world=raw_film.get("premiere_world"),
            premiere_world_country=raw_film.get("premiere_world_country"),
            rating_age_limits=raw_film.get("rating_age_limits"),
            rating_mpaa=raw_film.get("rating_mpaa"),
            seasons=[
                Season(
                    number=season.get("number"),
                    episodes=[
                        Episode(
                            episode_number=episode.get("episode_number"),
                            season_number=episode.get("season_number"),
                            name_en=episode.get("name_en"),
                            name_ru=episode.get("name_ru"),
                            release_date=datetime.strptime(
                                episode.get("release_date"), "&Y-&m-&d"
                            ) if episode.get("release_date") else None,
                            synopsis=episode.get("synopsis"),
                        )
                        for episode in season.get("episodes", [])
                    ]
                ) for season in raw_film.get("seasons", [])
            ],
            slogan=raw_film.get("slogan"),
            web_url=raw_film.get("web_url"),
        )

    @cached(ttl=43200, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def films_search_by_keyword(self, keyword: str, page: int = 1) -> Optional[Search]:
        params = {
            "keyword": keyword,
            "page": page
        }

        async with AsyncClient(headers=self.headers) as client:
            res = await client.get(self._films_search_by_keyword, params=params)
            if res.status_code == 200:
                data = res.json()
                return Search(
                    keyword=data["keyword"],
                    pages_count=data["pagesCount"],
                    search_films_count_result=data["searchFilmsCountResult"],
                    films=[self._parse_film(x) for x in data.get("films")],
                )

    @cached(ttl=43200, cache=RedisCache, serializer=PickleSerializer(), namespace="cache")
    async def film(self, film_id: int) -> Optional[DetailFilm]:
        async with AsyncClient(headers=self.headers) as client:
            res = await client.get(f"{self._films}/{film_id}")
            if res.status_code == 200:
                data = res.json()
                return self._parse_detailed_film(data["data"])
