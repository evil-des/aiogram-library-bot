from aiogram.fsm.state import State, StatesGroup


class BookAdding(StatesGroup):
    show_menu = State()
    set_genre = State()
    set_name = State()
    set_author = State()
    set_desc = State()
    confirm = State()


class BookListing(StatesGroup):
    all_books = State()
    filter_menu = State()
    filtered_books = State()

    book_info = State()
    delete_book = State()


class BookSearch(StatesGroup):
    query_input = State()
    result = State()
    book_info = State()
