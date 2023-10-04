from typing import List, Optional
from pydantic import BaseModel, AnyUrl


class Episode(BaseModel):
    number: str
    url: Optional[AnyUrl] = None


class Season(BaseModel):
    number: int
    episodes: List[Episode]
    url: AnyUrl


class SourceSeason(BaseModel):
    number: int
    episodes: List[Episode]


class Film(BaseModel):
    film_id: int
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    film_length: Optional[str] = None
    countries: List[str]
    genres: List[str]
    rating: Optional[str] = None
    poster_url: Optional[AnyUrl] = None
    url: Optional[AnyUrl] = None


class Serial(Film):
    seasons: List[Season]


class Source(BaseModel):
    film_id: int
    url: Optional[AnyUrl] = None
    seasons: Optional[List[SourceSeason]] = None
