from aiogram.fsm.state import State
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Group, Button, SwitchTo
from aiogram_dialog.widgets.text import Jinja, Const
from app.dialogs.common import CommonElements

from app.models import Book, Genre
from app.states.book import BookListing
from typing import Dict

from app.services.repo import Repo
from app.database.engine import AsyncSession


class BookInfoWindow(Window):
    def __init__(
        self,
        state: State
    ) -> None:
        super().__init__(
            self.get_detailed_book_info(),
            self.get_book_info_keyboard(),
            getter=self.get_book_data(),
            state=state
        )

    @staticmethod
    def get_book_info_keyboard():
        return Group(
            CommonElements.back_btn(),
            SwitchTo(
                Const("❌ Удалить"),
                id="delete_book",
                state=BookListing.delete_book
            ),
            width=2
        )

    def get_book_data(self):
        async def book_getter(
            dialog_manager: DialogManager,
            **kwargs
        ) -> Dict:
            repo: Repo = dialog_manager.middleware_data["repo"]
            book: Book = await repo.book_dao.get_book(
                dialog_manager.dialog_data.get("books_obj_id")
            )

            return {
                "name": book.name,
                "genre": book.genre.name,
                "author": book.author.full_name,
                "desc": book.desc
            }

        return book_getter

    @staticmethod
    def get_detailed_book_info() -> Jinja:
        return Jinja(
            "➖➖➖➖➖➖➖➖➖➖\n"
            "Название: <b>{{ name }}</b>\n"
            "Жанр: <b>{{ genre }}</b>\n"
            "Автор книги: <b>{{ author }}</b>\n\n"
            "Описание:\n<i>{{ desc }}</i>\n"
            "➖➖➖➖➖➖➖➖➖➖"
        )
