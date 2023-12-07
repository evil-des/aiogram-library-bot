from aiogram_dialog import Dialog
from app.states.book import BookListing
from app.models import BookFilter
from app.windows.listing import BooksWindow, GenresWindow
from app.windows import BookInfoWindow, BookDeleteWindow


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
