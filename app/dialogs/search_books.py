from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel
from aiogram_dialog.widgets.kbd import (
    Button, Group, Row, ScrollingGroup, Select, Back
)
from aiogram_dialog.widgets.input import (
    TextInput, MessageInput, ManagedTextInput
)
from app.dialogs.common import CommonElements
from aiogram_dialog import Dialog, Window, DialogManager
from app.states.book import BookListing, BookSearch
from app.services.repo import Repo
from app.models import BookFilter, Book
from app.windows.listing import BooksWindow, GenresWindow
from app.windows import BookInfoWindow, BookDeleteWindow
from typing import List, Any
import operator
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.text import Jinja


async def on_query_input_error(
    message: Message,
    dialog_manager: DialogManager,
    *args
) -> None:
    await message.answer("Ошибка: книга с такими ключевыми словами не найдена")


async def on_query_input_success(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    *args
) -> None:
    dialog_manager.dialog_data.update(key_word=widget.get_value())
    await dialog_manager.next()


dialog = Dialog(
    CommonElements.input(
        id="search_book",
        text=Const(
            "Введите запрос для поиска по книгам "
            "(может содержаться в названии, либо в имени автора):"
        ),
        state=BookSearch.query_input,
        on_success=on_query_input_success
    ),
    BooksWindow(
        state=BookSearch.show_result,
        filter=BookFilter(IS_KEY_WORD_FILTER=True)
    )
)
