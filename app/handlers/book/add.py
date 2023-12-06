from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from aiogram_dialog import (
    DialogManager, StartMode
)
from app.states.book import BookAdding

from app.services.repo import AsyncSession


router = Router()


@router.message(F.text == "➕ Добавить")
async def add_book(message: types.Message,
                   dialog_manager: DialogManager,
                   session: AsyncSession):
    await dialog_manager.start(
        BookAdding.show_menu,
        mode=StartMode.RESET_STACK
    )
