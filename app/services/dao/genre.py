from typing import List, Optional

from sqlalchemy.future import select

from app.models import Genre
from app.services.dao.base import DAO


class GenreDAO(DAO):
    async def get_genre(self, id: int = None, name: str = None) -> Optional[Genre]:
        if id is not None:
            q = select(Genre).filter_by(id=id)

        if name is not None:
            q = select(Genre).filter_by(name=name)

        return (await self.session.execute(q)).scalar()

    async def get_genres(self, ids: List[int] | None = None) -> Optional[List[Genre]]:
        q = select(Genre)
        if ids is not None:
            q.filter(Genre.id.in_(ids))
        return (await self.session.execute(q)).scalars().all()

    async def create_genre(self, name: str, desc: Optional[str] = None) -> Genre:
        async with self.session:
            genre = Genre(name=name, desc=desc)
            self.session.add(genre)
            await self.session.commit()
            await self.session.refresh(genre)
        return genre

    async def create_genre_if_not_exist(
        self, name: str, desc: Optional[str] = None
    ) -> Optional[Genre]:
        genre: Genre = await self.get_genre(name=name)
        if genre is None:
            return await self.create_genre(name, desc)

        return genre
