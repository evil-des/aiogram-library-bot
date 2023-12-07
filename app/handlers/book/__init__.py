from aiogram import Router, F
from . import add
from . import show
from . import search


def prepare_router() -> Router:
    book_router = Router(name=__name__)
    book_router.include_router(show.router)
    book_router.include_router(add.router)
    book_router.include_router(search.router)
    return book_router
