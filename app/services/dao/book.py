from typing import Optional, List

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, join

from app.models import (
    User, Book, Genre
)
from app.services.dao.base import DAO


class BookDAO(DAO):
    async def get_book(self, id: int) -> Optional[Book]:
        q = (
            select(Book)
            .filter_by(id=id)
        )
        return (await self.session.execute(q)).scalar()

    async def get_books(self, ids: List[int] | None = None) -> Optional[List[Book]]:
        q = select(Book)
        if ids is not None:
            q.filter(Book.id.in_(ids))
        return (await self.session.execute(q)).scalars().all()

    async def delete_book(self, id: int) -> None:
        q = delete(Book).where(
            Book.id == id
        )

        await self.session.execute(q)
        await self.session.commit()
        # await self.session.refresh(Book)
