from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


async def default_handler(event: types.TelegramObject, state: FSMContext) -> None:
    pass


def prepare_router() -> Router:
    default_router = Router(name=__name__)
    default_router.message.register(default_handler)

    return default_router
