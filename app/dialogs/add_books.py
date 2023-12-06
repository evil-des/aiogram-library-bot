from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel
from aiogram_dialog.widgets.kbd import (
    Button, Group, Row, ScrollingGroup, Select, Back
)
from aiogram_dialog.widgets.input import (
    TextInput, MessageInput, ManagedTextInput
)
from app.windows.listing import GenresWindow
from app.dialogs.common import CommonElements
from aiogram_dialog import Dialog, Window, DialogManager
from app.states.book import BookAdding
from app.services.repo import Repo
from app.models import Genre, Book
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.text import Jinja


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
    dialog_manager.dialog_data.update(name=widget.get_value())
    await dialog_manager.next()


async def on_author_name_success(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        *args
) -> None:
    dialog_manager.dialog_data.update(author=widget.get_value())
    await dialog_manager.next()


async def on_desc_success(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        *args
) -> None:
    dialog_manager.dialog_data.update(desc=widget.get_value())
    await dialog_manager.next()


async def get_book_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    repo: Repo = dialog_manager.middleware_data["repo"]
    genre: Genre = await repo.genre_dao.get_genre(
        data.get("genres_obj_id")
    )
    name = data.get("name").capitalize()
    author = " ".join([word.capitalize() for word in data.get("author").split()])

    if "desc" in data:
        desc = data.get("desc")
    else:
        desc = "Не указано"

    data.update(name=name, author=author)
    return {
        "name": name,
        "genre": genre,
        "author": author,
        "desc": desc,
    }


async def add_book(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
) -> None:
    await callback.answer("⏳ Ожидайте... Книга добавляется в базу данных")
    repo: Repo = dialog_manager.middleware_data["repo"]
    data = dialog_manager.dialog_data

    author = await repo.author_dao.create_author_if_not_exist(
        data.get("author")
    )

    book = Book(
        name=data.get("name"),
        desc=data.get("desc"),
        genre_id=data.get("genres_obj_id"),
        author_id=author.id,
    )

    await repo.user_dao.add_book(
        callback.from_user.id,
        book
    )

    await dialog_manager.done()
    await callback.message.answer("Книга успешно добавлена 👍")


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
    Window(
        Jinja(
            "➖➖➖➖➖➖➖➖➖➖\n"
            "Название: <b>{{ name }}</b>\n"
            "Жанр: <b>{{ genre.name }}</b>\n"
            "Автор книги: <b>{{ author }}</b>\n\n"
            "Описание:\n<i>{{ desc }}</i>\n"
            "➖➖➖➖➖➖➖➖➖➖\n\n"
            "📌 Проверьте правильность введенных данных и нажмите на нужную кнопку"
        ),
        Row(
          Button(Const("Добавить"), id="add_book", on_click=add_book),
          Button(Const("Отменить"), id="cancel", on_click=CommonElements.on_cancel_click),
        ),
        getter=get_book_data,
        state=BookAdding.confirm
    )
)
