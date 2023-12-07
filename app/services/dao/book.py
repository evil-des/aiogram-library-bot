from typing import List, Optional

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlmodel import col, or_

from app.models import Author, Book
from app.services.dao.base import DAO


class BookDAO(DAO):
    async def get_book(self, id: int) -> Optional[Book]:
        q = select(Book).filter_by(id=id)
        return (await self.session.execute(q)).scalar()

    async def get_books(
        self, ids: List[int] | None = None, key_word: str = None
    ) -> Optional[List[Book]]:
        q = select(Book)
        if ids is not None:
            q.filter(Book.id.in_(ids))

        if key_word is not None:
            key_word = key_word.lower()
            q = (
                select(Book)
                .join(Author, onclause=Author.id == Book.author_id)
                .where(
                    or_(
                        col(Book.name).ilike("%" + key_word + "%+"),
                        col(Author.full_name).ilike("%" + key_word + "%"),
                    )
                )
            )

        return (await self.session.execute(q)).scalars().all()

    async def delete_book(self, id: int) -> None:
        q = delete(Book).where(Book.id == id)

        await self.session.execute(q)
        await self.session.commit()
        # await self.session.refresh(Book)
