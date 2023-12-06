from aiogram import types, Router
from aiogram import F
from aiogram_dialog import (
    DialogManager, StartMode
)
from app.states.book import BookListing
from app.services.repo import AsyncSession

router = Router()


@router.message(F.text == "📚 Все книги")
async def show_books(message: types.Message,
                     dialog_manager: DialogManager,
                     session: AsyncSession):
    await dialog_manager.start(
        BookListing.all_books,
        mode=StartMode.RESET_STACK
    )
