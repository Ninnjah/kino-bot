from typing import List

from .base import BaseMethod
from ..models.model import PersonResponse, StaffResponse
from ..exceptions import BadRequest


class Staff(BaseMethod):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._base_url = f"{self._base_url}/staff".format(api_version="v1")

    async def by_film(self, film_id: int) -> List[StaffResponse]:
        res = await self.session._request_get(
            self._base_url, params={"filmId": film_id}
        )
        if res.status_code == 200:
            return [StaffResponse.model_validate(x) for x in res.json()]
        elif res.status_code == 404:
            return []
        else:
            raise BadRequest(res)

    async def get(self, person_id: int) -> PersonResponse:
        res = await self.session._request_get(f"{self._base_url}/{person_id}")
        if res.status_code == 200:
            return PersonResponse.model_validate(res.json())
        elif res.status_code == 404:
            return None
        else:
            raise BadRequest(res)
