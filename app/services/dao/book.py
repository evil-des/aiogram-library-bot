from typing import Optional, List

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, join

from app.models import (
    User, Book
)
from app.services.dao.base import DAO


class BookDAO(DAO):
    async def get_book(self, id: int) -> Optional[User]:
        q = (
            select(User)
            .filter_by(chat_id=chat_id)
        )
        return (await self.session.execute(q)).scalar()

    async def get_all_users(self) -> Optional[List[User]]:
        q = (select(User))
        return (await self.session.execute(q)).scalars().all()

    async def create_user(
            self,
            chat_id: int,
            full_name: str,
            username: str
    ) -> User:
        async with self.session:
            user = User(
                chat_id=chat_id,
                full_name=full_name,
                username=username
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def create_user_if_not_exist(
            self, chat_id: int
    ) -> User:
        user = await self.get_user(chat_id=chat_id)
        if user is None:
            return await self.create_user(chat_id=chat_id)
        return user

    async def update_user(
            self,
            chat_id: int,
            full_name: str = None,
            username: str = None
    ) -> User:
        user = await self.get_user(chat_id)
        async with self.session:
            if full_name is not None and \
                    user.full_name != full_name:
                user.full_name = full_name
            if username is not None and \
                    user.username != username:
                user.username = username

            await self.session.commit()
            await self.session.refresh(user)

        return user
