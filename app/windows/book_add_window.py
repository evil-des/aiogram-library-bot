from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Jinja

from app.dialogs.common import CommonElements
from app.models import Book, BookAdd
from app.services.repo import Repo
from app.states.book import BookListing


class BookAddWindow(Window):
    def __init__(self, state: State) -> None:
        super().__init__(
            self.get_detailed_book_info(),
            self.get_book_add_keyboard(self.add_book),
            getter=self.get_book_data,
            state=state,
        )

    @staticmethod
    async def get_book_data(dialog_manager: DialogManager, **kwargs):
        book_add: BookAdd = dialog_manager.dialog_data.get("book_add")
        book_add.name = book_add.name.capitalize()
        book_add.author = " ".join(
            [word.capitalize() for word in book_add.author.split()]
        )

        return {
            "name": book_add.name,
            "genre": book_add.genre,
            "author": book_add.author,
            "desc": book_add.desc,
        }

    @staticmethod
    def get_book_add_keyboard(on_add_click):
        return Row(
            CommonElements.add_btn(on_add_click),
            CommonElements.cancel_btn(),
        )

    @staticmethod
    def get_detailed_book_info() -> Jinja:
        return Jinja(
            "➖➖➖➖➖➖➖➖➖➖\n"
            "Название: <b>{{ name }}</b>\n"
            "Жанр: <b>{{ genre }}</b>\n"
            "Автор книги: <b>{{ author }}</b>\n\n"
            "Описание:\n<i>{{ desc }}</i>\n"
            "➖➖➖➖➖➖➖➖➖➖\n\n"
            "📌 Проверьте правильность введенных данных и нажмите на нужную кнопку"
        )

    @staticmethod
    async def add_book(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
    ) -> None:
        # await callback.answer("⏳ Ожидайте... Книга добавляется в базу данных")
        repo: Repo = dialog_manager.middleware_data["repo"]
        book_add: BookAdd = dialog_manager.dialog_data.get("book_add")

        author = await repo.author_dao.create_author_if_not_exist(book_add.author)

        book = Book(
            name=book_add.name,
            desc=book_add.desc,
            genre_id=book_add.genre_id,
            author=author,
        )
        await repo.user_dao.add_book(callback.from_user.id, book)

        await callback.answer("Книга успешно добавлена 👍")
        await dialog_manager.start(
            state=BookListing.all_books, mode=StartMode.RESET_STACK
        )
