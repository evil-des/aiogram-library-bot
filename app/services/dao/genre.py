from typing import Optional, List

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, join

from app.models import (
    User, Book, Genre
)
from app.services.dao.base import DAO


class GenreDAO(DAO):
    async def get_genre(self, id: int) -> Optional[Genre]:
        q = (
            select(Genre)
            .filter_by(id=id)
        )
        return (await self.session.execute(q)).scalar()

    async def get_genres(self, ids: List[int] | None = None) -> Optional[List[Genre]]:
        q = select(Genre)
        if ids is not None:
            q.filter(Genre.id.in_(ids))
        return (await self.session.execute(q)).scalars().all()

    async def create_genre(
            self,
            name: str,
            desc: Optional[str] = None
    ) -> Genre:
        async with self.session:
            genre = Genre(
                name=name,
                desc=desc
            )
            self.session.add(genre)
            await self.session.commit()
            await self.session.refresh(genre)
        return genre