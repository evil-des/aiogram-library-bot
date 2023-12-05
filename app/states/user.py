from aiogram.fsm.state import State, StatesGroup


class UserMainMenu(StatesGroup):
    # menu = State()
    start = State()
    all_books = State()
    search_book = State()
    add_book = State()
