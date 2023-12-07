from aiogram import Router

from . import start


def prepare_router() -> Router:
    user_router = Router(name=__name__)
    user_router.include_router(start.router)
    return user_router
