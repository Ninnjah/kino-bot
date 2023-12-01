import logging
from typing import Optional, Sequence, Union

from pydantic import ValidationError

from sqlalchemy import select, delete, bindparam
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy.engine.row import RowMapping

from tgbot.database.tables import User, Admin
from tgbot.database.films import Film

from tgbot.services.film_api.models.player import Film as FilmModel

logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    # users
    async def add_user(
            self,
            user_id: int,
            firstname: str,
            lastname: Optional[str],
            username: Optional[str]
    ) -> None:
        """Store user in DB, on conflict updates user information"""
        stmt = (
            insert(User)
            .values(
                user_id=user_id,
                firstname=firstname,
                lastname=lastname,
                username=username
            )
            .on_conflict_do_update(
                constraint=User.__table__.primary_key,
                set_={
                    "firstname": firstname,
                    "lastname": lastname,
                    "username": username
                }
            )
        )

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def get_user(self, user_id: int) -> Optional[RowMapping]:
        """Returns user from DB by user id"""
        stmt = select(User).where(User.user_id == user_id)

        res = await self.conn.execute(stmt)
        return res.mappings().one_or_none()

    async def list_users(self) -> Sequence[RowMapping]:
        """List all bot users"""
        stmt = select(User).order_by(User.created_on)

        res = await self.conn.execute(stmt)
        return res.mappings().all()

    # admins
    async def add_admin(self, user_id: int) -> None:
        """Store admin in DB, ignore duplicates

        :param user_id: User telegram id
        :type user_id: int
        """
        stmt = (
            insert(Admin)
            .values(user_id=user_id)
            .on_conflict_do_nothing()
        )

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def is_admin(self, user_id: int) -> bool:
        """Checks user is admin or not

        :param user_id: User telegram id
        :type user_id: int
        :return: User is admin boolean
        :rtype: bool
        """
        stmt = select(Admin).where(Admin.user_id == user_id)

        res = await self.conn.execute(stmt)
        res = res.mappings().one_or_none()
        return res is not None

    async def del_admin(self, user_id: int) -> None:
        """Delete admin from DB by user id

        :param user_id: User telegram id
        :type user_id: int
        :return: Deleted row count
        :rtype: int
        """
        stmt = delete(Admin).where(Admin.user_id == user_id)

        await self.conn.execute(stmt)
        await self.conn.commit()

    async def list_admins(self) -> Sequence[RowMapping]:
        """List all bot admins"""
        stmt = select(Admin)

        res = await self.conn.execute(stmt)
        return res.mappings().all()

    # films
    async def add_film(self, film_list: Union[Sequence[FilmModel], FilmModel]) -> None:
        if not isinstance(film_list, Sequence):
            film_list = [film_list]
        
        stmt = (
            insert(Film)
            .values(
                film_id=bindparam("film_id"),
                name_ru=bindparam("name_ru"),
                name_en=bindparam("name_en"),
                year=bindparam("year"),
                description=bindparam("description"),
                film_length=bindparam("film_length"),
                countries=bindparam("countries"),
                genres=bindparam("genres"),
                rating=bindparam("rating"),
                poster_url=bindparam("poster_url"),
                url=bindparam("url"),
            )
            .on_conflict_do_update(
                constraint=Film.__table__.primary_key,
                set_=dict(
                    name_ru=bindparam("name_ru"),
                    name_en=bindparam("name_en"),
                    year=bindparam("year"),
                    description=bindparam("description"),
                    film_length=bindparam("film_length"),
                    countries=bindparam("countries"),
                    genres=bindparam("genres"),
                    rating=bindparam("rating"),
                    poster_url=bindparam("poster_url"),
                    url=bindparam("url"),
                )
            )
        )
        
        await self.conn.execute(stmt, [film.model_dump(mode="json") for film in film_list])
        await self.conn.commit()
        return

    async def get_film(self, film_id: int) -> Optional[FilmModel]:
        stmt = select(Film).where(Film.film_id == film_id)

        res = await self.conn.execute(stmt)
        res = res.mappings().one_or_none()
        if res is None:
            return
        
        try:
            return FilmModel.model_validate(dict(res))
        except ValidationError as e:
            logger.warning(f"GET_FILM VALIDATION ERROR: {e}", exc_info=True)
            return

    async def list_films(self) -> Sequence[RowMapping]:
        stmt = select(Film).order_by(Film.created_on)

        res = await self.conn.execute(stmt)
        return res.mappings().all()

    async def search_films(self, films_id: Sequence[int]) -> Sequence[RowMapping]:
        stmt = select(Film).where(Film.film_id.in_(films_id))

        res = await self.conn.execute(stmt)
        return res.mappings().all()
