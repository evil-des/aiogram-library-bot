import asyncio

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from app.keyboards import Menu
from app.services.repo import Repo
from app.states.user import UserMainMenu

router = Router()


@router.message(CommandStart())
async def start(
    message: types.Message, dialog_manager: DialogManager, repo: Repo
) -> None:
    await repo.user_dao.create_user_if_not_exist(
        chat_id=message.chat.id,
        full_name=message.chat.full_name,
        username=message.chat.username,
    )
    await dialog_manager.start(UserMainMenu.start, mode=StartMode.RESET_STACK)
    await wait_and_send(message)


async def wait_and_send(message: types.Message):
    await asyncio.sleep(3)
    await message.answer(
        "Ознакомься с интерфейсом нашего бота, "
        "затем можешь приступать к добавлению книг 😎",
        reply_markup=Menu.main(),
    )
