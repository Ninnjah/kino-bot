from .base import BaseMethod
from ..models.model import KinopoiskUserVoteResponse
from ..exceptions import BadRequest


class KpUsers(BaseMethod):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._base_url = f"{self._base_url}/kp_users".format(api_version="v1")

    async def votes(self, user_id: int, page: int = 1) -> KinopoiskUserVoteResponse:
        res = await self.session._request_get(
            f"{self._base_url}/{user_id}", params={"page": page}
        )
        if res.status_code == 200:
            return KinopoiskUserVoteResponse.model_validate(res.json())
        else:
            raise BadRequest(res)
