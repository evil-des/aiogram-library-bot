from typing import List, Optional

from sqlalchemy.future import select

from app.models import Author
from app.services.dao.base import DAO


class AuthorDAO(DAO):
    async def get_author(
        self, id: int = None, full_name: str = None
    ) -> Optional[Author]:
        if id is None and full_name is None:
            raise Exception("Укажите ID, либо full_name автора")

        if id is not None:
            q = select(Author).filter_by(id=id)

        if full_name is not None:
            q = select(Author).filter_by(full_name=full_name)

        return (await self.session.execute(q)).scalar()

    async def get_authors(self, ids: List[int] | None = None) -> Optional[List[Author]]:
        q = select(Author)
        if ids is not None:
            q.filter(Author.id.in_(ids))
        return (await self.session.execute(q)).scalass().all()

    async def create_author(self, full_name: str) -> Author:
        async with self.session:
            author = Author(full_name=full_name)
            self.session.add(author)
            await self.session.commit()
            await self.session.refresh(author)
        return author

    async def create_author_if_not_exist(self, full_name: str) -> Author:
        author = await self.get_author(full_name=full_name)
        if author is None:
            return await self.create_author(
                full_name=full_name,
            )
        return author
