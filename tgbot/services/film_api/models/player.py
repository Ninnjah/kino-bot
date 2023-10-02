from typing import List
from pydantic import BaseModel, AnyUrl


Source = AnyUrl


class Episode(BaseModel):
    number: int
    url: AnyUrl


class Season(BaseModel):
    number: int
    episodes: List[Episode]
