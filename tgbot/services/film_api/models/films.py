from datetime import date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, AnyUrl


class FilmType(str, Enum):
    FILM = "FILM"
    film = "film"
    TV_SHOW = "TV_SHOW"
    TV_SERIES = "TV_SERIES"
    SERIES = "series"
    CARTOON_SERIES = "cartoon-series"
    MINI_SERIES = "MINI_SERIES"
    VIDEO = "VIDEO"
    UNKNOWN = "UNKNOWN"


class Episode(BaseModel):
    episode_number: int
    season_number: int
    name_en: Optional[str] = None
    name_ru: Optional[str] = None
    release_date: Optional[date] = None
    synopsis: Optional[str] = None


class Season(BaseModel):
    number: int
    episodes: List[Episode]


class Film(BaseModel):
    film_id: int
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    type: FilmType
    year: Optional[int] = None
    description: Optional[str] = None
    film_length: Optional[str] = None
    countries: List[str]
    genres: List[str]
    rating: Optional[str] = None
    rating_vote_count: Optional[int] = None
    poster_url: Optional[AnyUrl] = None
    poster_url_preview: Optional[AnyUrl] = None


class DetailFilm(Film):
    distributor_release: Optional[str] = None
    distributors: Optional[str] = None
    facts: Optional[List[str]] = None
    premiere_bluray: Optional[bool] = None
    premiere_digital: Optional[bool] = None
    premiere_dvd: Optional[bool] = None
    premiere_ru: Optional[date] = None
    premiere_world: Optional[date] = None
    premiere_world_country: Optional[str] = None
    rating_age_limits: Optional[int] = None
    rating_mpaa: Optional[str] = None
    seasons: Optional[List[Season]] = None
    slogan: Optional[str] = None
    web_url: Optional[AnyUrl] = None


class Serial(Film):
    seasons: Optional[List[Season]] = None


class Search(BaseModel):
    keyword: str
    pages_count: int
    search_films_count_result: int
    films: List[Film]
