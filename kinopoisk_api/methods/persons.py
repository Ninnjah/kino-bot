from .base import BaseMethod
from ..models.model import PersonByNameResponse
from ..exceptions import BadRequest


class Persons(BaseMethod):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._base_url = f"{self._base_url}/persons".format(api_version="v1")

    async def get(self, name: str, page: int = 1) -> PersonByNameResponse:
        res = await self.session._request_get(
            self._base_url, params={"name": name, "page": page}
        )
        if res.status_code == 200:
            return PersonByNameResponse.model_validate(res.json())
        else:
            raise BadRequest(res)
