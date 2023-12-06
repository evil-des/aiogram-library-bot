from sqlalchemy.ext.asyncio import AsyncSession

from app.services.dao import (
    UserDAO, GenreDAO, AuthorDAO
)

from aiocache import Cache


class Repo:
    def __init__(self, session: AsyncSession, cache: Cache):
        self.session = session
        self.user_dao = UserDAO(session=session)
        self.genre_dao = GenreDAO(session=session)
        self.author_dao = AuthorDAO(session=session)
