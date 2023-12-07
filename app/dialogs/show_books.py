from aiogram_dialog import Dialog

from app.models import BookFilter
from app.states.book import BookListing
from app.windows import BookDeleteWindow, BookInfoWindow
from app.windows.listing import BooksWindow, GenresWindow

dialog = Dialog(
    BooksWindow(state=BookListing.all_books, switch_to=BookListing.book_info),
    BookInfoWindow(state=BookListing.book_info),
    BookDeleteWindow(state=BookListing.delete_book),
    GenresWindow(state=BookListing.filter_menu, switch_to=BookListing.filtered_books),
    BooksWindow(
        state=BookListing.filtered_books,
        filter=BookFilter(IS_GENRE_FILTER=True),
        switch_to=BookListing.book_info,
    ),
)
