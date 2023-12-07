from .base import BaseListingWindow
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager
from app.services.repo import Repo
from app.models import Book
from typing import List, Any


class BooksWindow(BaseListingWindow):
    LISTING_MESSAGE = "Выберите книгу из списка (всего {count} шт.):"
    BUTTON_TEXT = "{item.name} ({item.author.full_name})"

    def __init__(self, state: State):
        super().__init__(id="books", state=state)

    @staticmethod
    async def get_data(dialog_manager: DialogManager, **kwargs):
        repo: Repo = dialog_manager.middleware_data["repo"]
        books: List[Book] = await repo.book_dao.get_books()

        return {
            "items": books,
            "count": len(books)
        }
