from .base import BaseListingWindow
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const
from app.states.book import BookListing
from app.services.repo import Repo
from app.models import Book, BookFilter
from typing import List, Any, Optional


class BooksWindow(BaseListingWindow):
    LISTING_MESSAGE = "Выберите книгу из списка (всего {count} шт.):"
    BUTTON_TEXT = "{item.name} ({item.author.full_name})"

    def __init__(self, state: State, filter: BookFilter = None):
        elements = None
        if filter is None:
            elements = [self.get_filter_keyboard()]

        super().__init__(
            id="books",
            state=state,
            elements=elements,
            data_getter_kwargs={"filter": filter},
            switch_to=BookListing.book_info
        )

    @staticmethod
    def get_filter_keyboard():
        return SwitchTo(
            Const("🔖 Фильтр по жанру"),
            id="filter_menu",
            state=BookListing.filter_menu
        )

    @staticmethod
    async def get_filtered_items(
        dialog_manager: DialogManager,
        filter: BookFilter
    ) -> Optional[List[Book]]:
        books = []
        repo: Repo = dialog_manager.middleware_data["repo"]

        if filter.IS_GENRE_FILTER:
            books: List[Book] = (
                await repo.genre_dao.get_genre(
                    dialog_manager.dialog_data.get("genres_obj_id")
                )
            ).books
        if filter.IS_KEY_WORD_FILTER:
            books: List[Book] = await repo.book_dao.get_books(
                key_word=dialog_manager.dialog_data.get("key_word")
            )

        return books

    def data_getter(self, filter: BookFilter = None):
        async def get_data(dialog_manager: DialogManager, **kwargs):
            repo: Repo = dialog_manager.middleware_data["repo"]
            books: Optional[List[Book]] = []

            if filter is None:
                books = await repo.book_dao.get_books()

            if filter is not None:
                books = await self.get_filtered_items(dialog_manager, filter)

            return {
                "items": books,
                "count": len(books)
            }
        return get_data
