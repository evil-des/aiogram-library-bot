from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import QueuePool
from sqlmodel import SQLModel


def get_engine(db_url: str) -> AsyncEngine:
    engine = create_async_engine(
        db_url, pool_size=20, max_overflow=0, poolclass=QueuePool
    )
    return engine


def get_async_session_maker(db_url: PostgresDsn) -> async_sessionmaker:
    engine = get_engine(db_url=db_url.unicode_string())
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db(engine):
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
