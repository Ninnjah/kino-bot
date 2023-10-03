from typing import List, Optional
from pydantic import BaseModel, AnyUrl


class Episode(BaseModel):
    number: int
    url: AnyUrl


class Season(BaseModel):
    number: int
    episodes: List[Episode]


class Source(BaseModel):
    film_id: int
    url: Optional[AnyUrl] = None
    seasons: Optional[List[Season]] = None
