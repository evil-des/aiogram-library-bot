from aiogram import Router, F
from . import add


def prepare_router() -> Router:
    book_router = Router(name=__name__)
    book_router.include_router(add.router)
    return book_router
