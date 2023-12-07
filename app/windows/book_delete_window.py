from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row

from app.dialogs.common import CommonElements
from app.models import Book, Genre, BookAdd
from app.states.book import BookListing
from aiogram_dialog.widgets.text import Jinja, Const
from typing import Dict

from app.services.repo import Repo


class BookDeleteWindow(Window):
    def __init__(
        self,
        state: State
    ) -> None:
        super().__init__(
            Const("Вы действительно хотите удалить эту книгу?"),
            self.get_book_delete_keyboard(self.delete_book),
            state=state
        )

    @staticmethod
    def get_book_delete_keyboard(on_confirm_click):
        return CommonElements.confirm_n_cancel(
            on_click=on_confirm_click
        )

    @staticmethod
    async def delete_book(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
    ) -> None:
        # await callback.answer("⏳ Ожидайте... Книга удаляется из базы данных")
        repo: Repo = dialog_manager.middleware_data["repo"]
        book_id: int = dialog_manager.dialog_data.get("books_obj_id")

        await repo.book_dao.delete_book(book_id)

        await callback.answer("Книга успешно удалена 👍")
        await dialog_manager.start(
            state=BookListing.all_books,
            mode=StartMode.RESET_STACK
        )
