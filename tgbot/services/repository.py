import logging
from typing import Optional, Sequence, Union

from pydantic import ValidationError

from sqlalchemy import select, delete, bindparam, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy.engine.row import RowMapping

from tgbot.database.tables import User, Admin
from tgbot.database.films import Film, Source
from tgbot.database.admin import Player

from tgbot.services.film_api.models import Film as FilmModel
from tgbot.services.film_api.models import Source as SourceModel

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
        username: Optional[str],
    ) -> None:
        """Store user in DB, on conflict updates user information"""
        stmt = (
            insert(User)
            .values(
                id=user_id,
                firstname=firstname,
                lastname=lastname,
                username=username,
            )
            .on_conflict_do_update(
                constraint=User.__table__.primary_key,
                set_={
                    "firstname": firstname,
                    "lastname": lastname,
                    "username": username,
                },
            )
        )

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def get_user(self, user_id: int) -> Optional[RowMapping]:
        """Returns user from DB by user id"""
        stmt = select(User).where(User.id == user_id)

        res = await self.conn.execute(stmt)
        return res.mappings().one_or_none()

    async def list_users(self) -> Sequence[RowMapping]:
        """List all bot users"""
        stmt = select(User).order_by(User.created_on)

        res = await self.conn.execute(stmt)
        return res.mappings().all()

    # admins
    async def add_admin(self, user_id: int, sudo: bool = False) -> None:
        """Store admin in DB, ignore duplicates

        :param user_id: User telegram id
        :type user_id: int
        :param sudo: Super user privileges
        :type sudo: bool
        """
        stmt = insert(Admin).values(id=user_id, sudo=sudo).on_conflict_do_nothing()

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def set_admin_sudo(self, user_id: int, sudo: bool) -> None:
        """Set admin sudo status

        :param user_id: User telegram id
        :type user_id: int
        :param sudo: Super user privileges
        :type sudo: bool
        """
        stmt = update(Admin).values(sudo=sudo).where(Admin.id == user_id)

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def is_admin(self, user_id: int) -> Optional[RowMapping]:
        """Checks user is admin or not

        :param user_id: User telegram id
        :type user_id: int
        :return: User is admin boolean
        :rtype: bool
        """
        stmt = select(Admin).where(Admin.id == user_id)

        res = await self.conn.execute(stmt)
        res = res.mappings().one_or_none()
        return res

    async def del_admin(self, user_id: int) -> None:
        """Delete admin from DB by user id

        :param user_id: User telegram id
        :type user_id: int
        :return: Deleted row count
        :rtype: int
        """
        stmt = delete(Admin).where(Admin.id == user_id)

        await self.conn.execute(stmt)
        await self.conn.commit()

    async def get_admin(self, user_id: int) -> Optional[RowMapping]:
        """Returns admin from DB by user id"""
        stmt = select(Admin).where(Admin.id == user_id)

        res = await self.conn.execute(stmt)
        return res.mappings().one_or_none()

    async def list_admins(self) -> Sequence[RowMapping]:
        """List all bot admins"""
        stmt = (
            select(Admin).order_by(Admin.sudo.desc()).order_by(Admin.updated_on.desc())
        )

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
                type=bindparam("type"),
                year=bindparam("year"),
                description=bindparam("description"),
                film_length=bindparam("film_length"),
                countries=bindparam("countries"),
                genres=bindparam("genres"),
                rating=bindparam("rating"),
                rating_vote_count=bindparam("rating_vote_count"),
                poster_url=bindparam("poster_url"),
                poster_url_preview=bindparam("poster_url_preview"),
            )
            .on_conflict_do_update(
                constraint=Film.__table__.primary_key,
                set_=dict(
                    name_ru=bindparam("name_ru"),
                    name_en=bindparam("name_en"),
                    type=bindparam("type"),
                    year=bindparam("year"),
                    description=bindparam("description"),
                    film_length=bindparam("film_length"),
                    countries=bindparam("countries"),
                    genres=bindparam("genres"),
                    rating=bindparam("rating"),
                    rating_vote_count=bindparam("rating_vote_count"),
                    poster_url=bindparam("poster_url"),
                    poster_url_preview=bindparam("poster_url_preview"),
                ),
            )
        )

        await self.conn.execute(
            stmt, [film.model_dump(mode="json") for film in film_list]
        )
        await self.conn.commit()
        return

    async def get_film(self, film_id: int) -> Optional[FilmModel]:
        stmt = select(Film).where(Film.film_id == film_id)
        source_stmt = select(Source).where(Source.film_id == film_id)

        try:
            res = await self.conn.execute(stmt)
            res = res.mappings().one_or_none()
            if res is None:
                return
            source_res = await self.conn.execute(source_stmt)
            source_res = source_res.mappings().all()

            film = FilmModel.model_validate(dict(res))
            if source_res:
                film.source = [
                    SourceModel.model_validate(dict(source)) for source in source_res
                ]

            return film

        except (ValidationError, DatabaseError) as e:
            logger.warning(f"GET_FILM {e}", exc_info=True)
            return

    async def list_films(
        self, films_id: Optional[Sequence[int]] = None
    ) -> Sequence[FilmModel]:
        if films_id:
            stmt = (
                select(Film).where(Film.film_id.in_(films_id)).order_by(Film.created_on)
            )
        else:
            stmt = select(Film).order_by(Film.created_on)
        source_stmt = select(Source).where(Source.film_id.in_(films_id))

        res = await self.conn.execute(stmt)
        source_res = await self.conn.execute(source_stmt)

        films = []
        raw_films = [FilmModel.model_validate(film) for film in res.mappings().all()]
        sources = [
            SourceModel.model_validate(source) for source in source_res.mappings().all()
        ]
        for film in raw_films:
            source = list(filter(lambda x: x.film_id == film.film_id, sources))
            if source:
                film.source = source
            films.append(film)

        return films

    async def search_films(self, films_id: Sequence[int]) -> Sequence[FilmModel]:
        stmt = (
            select(Film)
            .join(Source, Source.film_id == Film.film_id)
            .where(Film.film_id.in_(films_id))
            .distinct()
        )

        res = await self.conn.execute(stmt)
        return [FilmModel.model_validate(film) for film in res.mappings().all()]

    async def add_source(self, source_list: Union[Sequence[SourceModel], SourceModel]):
        if not isinstance(source_list, Sequence):
            source_list = [source_list]

        stmt = (
            insert(Source)
            .values(
                title=bindparam("title"),
                url=bindparam("url"),
                film_id=bindparam("film_id"),
            )
            .on_conflict_do_update(
                constraint="unique_source",
                set_=dict(
                    title=bindparam("title"),
                    url=bindparam("url"),
                    film_id=bindparam("film_id"),
                ),
            )
        )

        await self.conn.execute(
            stmt, [source.model_dump(mode="json") for source in source_list]
        )
        await self.conn.commit()
        return

    # players
    async def init_players(self, players: Sequence[str]) -> None:
        stmt = insert(Player).values(title=bindparam("title")).on_conflict_do_nothing()

        await self.conn.execute(stmt, [{"title": x} for x in players])
        await self.conn.commit()

    async def toggle_player(self, player_title: str, is_active: bool) -> None:
        stmt = (
            update(Player)
            .where(Player.title == player_title)
            .values(is_active=is_active)
        )

        await self.conn.execute(stmt)
        await self.conn.commit()

    async def list_players(self) -> Sequence[RowMapping]:
        stmt = select(Player).order_by(Player.title)

        res = await self.conn.execute(stmt)
        return res.mappings().all()
