from httpx import AsyncClient


class BaseMethod:
    def __init__(self, base_url: str, session: AsyncClient):
        self._base_url = base_url
        self.session = session
