from aiogram import types, Router
from aiogram import F
from aiogram_dialog import (
    DialogManager, StartMode
)
from app.states.book import BookSearch

router = Router()


@router.message(F.text == "🔎 Поиск книг")
async def search_book(message: types.Message,
                      dialog_manager: DialogManager):
    await dialog_manager.start(
        BookSearch.query_input,
        mode=StartMode.RESET_STACK
    )
