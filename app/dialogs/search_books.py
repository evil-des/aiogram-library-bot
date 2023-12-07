from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.text import Const

from app.dialogs.common import CommonElements
from app.models import BookFilter
from app.states.book import BookSearch
from app.windows import BookInfoWindow
from app.windows.listing import BooksWindow


async def on_query_input_error(
    message: Message, dialog_manager: DialogManager, *args
) -> None:
    await message.answer("Ошибка: книга с такими ключевыми словами не найдена")


async def on_query_input_success(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, *args
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
        on_success=on_query_input_success,
    ),
    BooksWindow(
        state=BookSearch.result,
        filter=BookFilter(IS_KEY_WORD_FILTER=True),
        switch_to=BookSearch.book_info,
    ),
    BookInfoWindow(state=BookSearch.book_info),
)
