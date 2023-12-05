from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from aiogram_dialog import (
    DialogManager, StartMode, Dialog, Window
)
from aiogram_dialog.widgets.text import Const, Format
from app import states
from app.db import AsyncSession
from .register_user import register_user


window = Window(
    Const("test"),
    state=states.user.UserMainMenu.menu,
)

router = Router()
dialog = Dialog(window)


@router.message(Command("start"))
async def start(message: types.Message,
                dialog_manager: DialogManager, db_session: AsyncSession):
    await register_user(message, db_session)
    await dialog_manager.start(states.user.UserMainMenu.menu)
