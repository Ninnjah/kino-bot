from .base import BaseMethod
from ..models.model import ApiKeyResponse
from ..exceptions import BadRequest


class ApiKeys(BaseMethod):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._base_url = f"{self._base_url}/api_keys".format(api_version="v1")

    async def get(self, api_key: str) -> ApiKeyResponse:
        res = await self.session._request_get(f"{self._base_url}/{api_key}")
        if res.status_code == 200:
            return ApiKeyResponse.model_validate(res.json())
        else:
            raise BadRequest(res)
