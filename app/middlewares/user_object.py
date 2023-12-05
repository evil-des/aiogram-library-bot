from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User


class UserObjectMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if event.message is None:
            return await handler(event, data)

        # TODO save into cache
        if isinstance(event, Update):
            query = select(User).where(User.chat_id == event.message.chat.id)
        else:
            query = select(User).where(User.chat_id == event.chat.id)

        session: AsyncSession = data.get("db_session")
        result = await session.execute(query)

        user: User = result.scalar()
        data["user"] = user

        return await handler(event, data)
