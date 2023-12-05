from aiogram import Router
from aiogram.filters import CommandStart
from . import start
from aiogram_dialog import setup_dialogs


def prepare_router() -> Router:
    user_router = Router(name=__name__)
    # сначала все роутеры
    user_router.include_router(start.router)

    # затем все диалоги
    user_router.include_router(start.dialog)
    setup_dialogs(user_router)

    return user_router
