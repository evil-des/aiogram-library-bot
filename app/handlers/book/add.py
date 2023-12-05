from aiogram import types, Router
from aiogram.filters import Command
from aiogram import F

from aiogram_dialog import (
    DialogManager, StartMode, Dialog, Window
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Group, Row
from app.states.user import UserMainMenu
from app.states.book import BookAdding

from app.db import AsyncSession
from app.models import User


router = Router()


@router.message(F.text == "➕ Добавить")
async def add_book(message: types.Message,
                   dialog_manager: DialogManager,
                   db_session: AsyncSession,
                   user: User):
    await dialog_manager.start(
        BookAdding.show_menu,
        mode=StartMode.RESET_STACK
    )
