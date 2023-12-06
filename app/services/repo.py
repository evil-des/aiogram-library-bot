from sqlalchemy.ext.asyncio import AsyncSession

from app.services.dao import (
    UserDAO, GenreDAO
)

from aiocache import Cache


class Repo:
    def __init__(self, session: AsyncSession, cache: Cache):
        self.session = session
        self.user_dao = UserDAO(session=session)
        self.genre_dao = GenreDAO(session=session)
