from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel
from aiogram_dialog.widgets.kbd import (
    Button, Group, Row, ScrollingGroup, Select, Back
)
from aiogram_dialog.widgets.input import (
    TextInput, MessageInput, ManagedTextInput
)
from app.windows import BookConfirmWindow
from app.windows.listing import GenresWindow
from app.dialogs.common import CommonElements
from aiogram_dialog import Dialog, Window, DialogManager
from app.states.book import BookAdding
from app.services.repo import Repo
from app.models import Genre, Book, BookAdd
from aiogram.types import CallbackQuery, Message


def author_name_input_checker(text: str):
    if all(x.isspace() or x.isalpha() for x in text):
        return text
    raise ValueError


async def on_author_input_error(message: Message, *args) -> None:
    await message.answer("Ошибка: в имени автора разрешены только буквы и пробелы")


async def on_name_success(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        *args
) -> None:
    repo: Repo = dialog_manager.middleware_data["repo"]
    data = dialog_manager.dialog_data

    book_add = BookAdd(name=widget.get_value(), genre_id=data.get("genres_obj_id"))
    book_add.genre = (await repo.genre_dao.get_genre(book_add.genre_id)).name
    data.update(book_add=book_add)

    await dialog_manager.next()


async def on_author_name_success(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        *args
) -> None:
    book_add: BookAdd = dialog_manager.dialog_data.get("book_add")
    book_add.author = widget.get_value()
    await dialog_manager.next()


async def on_desc_success(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        *args
) -> None:
    book_add: BookAdd = dialog_manager.dialog_data.get("book_add")
    book_add.desc = widget.get_value()
    await dialog_manager.next()


dialog = Dialog(
    Window(
        Const("Перед вами открылось меню добавления новых книг!\n\n"
              "Чтобы продолжить, нажмите соответствующую кнопку, либо нажмите <b>Отмена</b>"),
        Row(
            SwitchTo(
                text=Const("Продолжить"),
                id="show_genres",
                state=BookAdding.set_genre
            ),
            Cancel(Const("Отмена"), on_click=CommonElements.on_cancel_click),
        ),
        state=BookAdding.show_menu,
    ),
    GenresWindow(
        state=BookAdding.set_genre
    ),
    CommonElements.input(
        id="book_name",
        text=Const("Теперь напишите название вашей книги:"),
        state=BookAdding.set_name,
        on_success=on_name_success
    ),
    CommonElements.input(
        id="author_name",
        text=Const("Укажите автора книги (не допускаются какие-либо символы, кроме пробела и букв):"),
        state=BookAdding.set_author,
        type_factory=author_name_input_checker,
        on_success=on_author_name_success,
        on_error=on_author_input_error
    ),
    CommonElements.input(
        id="author_name",
        text=Const("Введите описание книги, либо <b>пропустите</b> этот шаг:"),
        state=BookAdding.set_desc,
        on_success=on_desc_success,
        skip=True
    ),
    BookConfirmWindow(
        state=BookAdding.confirm
    )
)
