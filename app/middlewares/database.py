from aiocache import Cache
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Awaitable, Dict, Any
from app.services.repo import Repo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, async_session_maker, cache: Cache):
        super().__init__()
        self.async_session_maker = async_session_maker
        self.cache = cache

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = self.async_session_maker()
        data["session"] = session
        data["repo"] = Repo(session=session, cache=self.cache)
        return await handler(event, data)
