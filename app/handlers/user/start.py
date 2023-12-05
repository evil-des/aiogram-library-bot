from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from aiogram_dialog import (
    DialogManager, StartMode, Dialog, Window
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Group
from app import states
from app.db import AsyncSession
from .register_user import register_user
import asyncio

from app.keyboards import Menu

window = Window(
    Format("Приветствуем тебя, @{start_data[username]} ✌️\n\n"
           "Этот телеграмм-бот поможет тебе "
           "больше не держать названия любимых книг в голове :)\n\n"
           "Теперь ты можешь добавлять их в базу данных нашей библиотеки, "
           "а затем осуществлять удобный поиск по ней!"),
    state=states.user.UserMainMenu.menu,
)

router = Router()
dialog = Dialog(window)


@router.message(Command("start"))
async def start(message: types.Message,
                dialog_manager: DialogManager, db_session: AsyncSession):
    user = await register_user(message, db_session)
    await dialog_manager.start(
        states.user.UserMainMenu.menu,
        data={"username": user.username}
    )
    await wait_and_send(message)


async def wait_and_send(message: types.Message):
    await asyncio.sleep(5)
    await message.answer(
        "Ознакомься с интерфейсом нашего бота, "
        "затем можешь приступать к добавлению книг 😎",
        reply_markup=Menu.main()
    )
