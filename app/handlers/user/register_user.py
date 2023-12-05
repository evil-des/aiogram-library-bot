from aiogram import types
from app.db import AsyncSession
from app.models import User
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.future import select


async def register_user(message: types.Message,
                        db_session: AsyncSession) -> User:
    username = validate_username(message.chat.username)
    user = User(
        chat_id=message.chat.id,
        username=username,
        full_name=message.chat.full_name
    )

    db_session.add(user)

    try:
        await db_session.commit()
        await db_session.refresh(user)
    except IntegrityError:
        await update_user(message, db_session)
        await db_session.rollback()
    except PendingRollbackError:
        await db_session.rollback()

    return user


async def update_user(message: types.Message,
                      db_session: AsyncSession) -> User:
    # result = await db_session.execute(select(User).where(User.chat_id == message.chat.id))
    user = db_session.query(User).filter(User.chat_id == message.chat.id).first()
    if user:
        user.username = validate_username(message.chat.username)
        user.full_name = message.chat.full_name

        try:
            await db_session.commit()
            await db_session.refresh(user)
        except PendingRollbackError:
            await db_session.rollback()

    return user


def validate_username(username):
    if username:
        return username.lower()
    return None