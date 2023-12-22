from typing import Optional
from httpx import AsyncClient

from .client.session.httpx import HttpxSession
from .methods.films import Films
from .methods.staff import Staff
from .methods.persons import Persons
from .methods.kp_users import KpUsers
from .methods.api_keys import ApiKeys


class KinopoiskAPI:
    def __init__(self, token: str, session: Optional[AsyncClient] = None):
        self.token = token
        self.headers = {"X-API-KEY": self.token}
        self.session = session or HttpxSession(headers=self.headers)

        self._base_url = "https://kinopoiskapiunofficial.tech/api/{api_version}"

        self.films = Films(base_url=self._base_url, session=self.session)
        self.staff = Staff(base_url=self._base_url, session=self.session)
        self.persons = Persons(base_url=self._base_url, session=self.session)
        self.kp_users = KpUsers(base_url=self._base_url, session=self.session)
        self.api_keys = ApiKeys(base_url=self._base_url, session=self.session)
