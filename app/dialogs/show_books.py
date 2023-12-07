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
from app.states.book import BookListing
from app.services.repo import Repo
from app.models import BookFilter
from app.windows.listing import BooksWindow, GenresWindow
from app.windows import BookInfoWindow, BookDeleteWindow
from typing import List, Any
import operator
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.text import Jinja


dialog = Dialog(
    BooksWindow(
        state=BookListing.all_books
    ),
    BookInfoWindow(
        state=BookListing.book_info
    ),
    BookDeleteWindow(
        state=BookListing.delete_book
    ),
    GenresWindow(
        state=BookListing.filter_menu,
        switch_to=BookListing.filtered_books
    ),
    BooksWindow(
        state=BookListing.filtered_books,
        filter=BookFilter(IS_GENRE_FILTER=True)
    )
)
