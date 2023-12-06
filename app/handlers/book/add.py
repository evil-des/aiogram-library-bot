from aiogram import types, Router
from aiogram import F
from aiogram_dialog import (
    DialogManager, StartMode
)
from app.states.book import BookAdding

router = Router()


@router.message(F.text == "➕ Добавить")
async def add_book(message: types.Message,
                   dialog_manager: DialogManager):
    await dialog_manager.start(
        BookAdding.show_menu,
        mode=StartMode.RESET_STACK
    )
