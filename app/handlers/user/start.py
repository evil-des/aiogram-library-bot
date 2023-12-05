from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from aiogram_dialog import (
    DialogManager, StartMode
)
from app.states.user import UserMainMenu
from app.db import AsyncSession
from app.models import User
from .register_user import register_user, update_user
import asyncio

from app.keyboards import Menu

router = Router()


@router.message(Command("start"))
async def start(message: types.Message,
                dialog_manager: DialogManager,
                db_session: AsyncSession,
                user: User):
    if not user:
        await register_user(message, db_session)
    else:
        await update_user(message, db_session)

    await dialog_manager.start(
        UserMainMenu.start,
        mode=StartMode.RESET_STACK
    )
    await wait_and_send(message)


async def wait_and_send(message: types.Message):
    await asyncio.sleep(3)
    await message.answer(
        "Ознакомься с интерфейсом нашего бота, "
        "затем можешь приступать к добавлению книг 😎",
        reply_markup=Menu.main()
    )
