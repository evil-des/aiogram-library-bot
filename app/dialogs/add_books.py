from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel
from aiogram_dialog.widgets.kbd import (
    Button, Group, Row, ScrollingGroup, Select
)
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog import Dialog, Window, DialogManager
from app.states.book import BookAdding
from app.db import async_session
from app.models import Genre
from sqlalchemy.future import select
from typing import List, Any
import operator
from aiogram.types import CallbackQuery, Message


async def get_genres(**kwargs):
    async with async_session() as session:
        result = await session.execute(select(Genre))
        genres = result.scalars().all()
        for genre in genres:
            print(genre.name)
    return {
        "genres": genres,
        "count": len(genres)
    }


async def on_cancel_click(c: CallbackQuery, widget, dialog_manager: DialogManager,
                          *args, **kwargs):
    await dialog_manager.reset_stack()
    await c.message.delete()


async def on_genre_click(callback: CallbackQuery, widget: Any,
                         dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["genre_id"] = item_id
    await dialog_manager.start(BookAdding.set_name)


async def on_name_input(message: Message, widget: Any,
                        dialog_manager: DialogManager, data):
    dialog_manager.dialog_data["name"] = message.text
    await dialog_manager.start(BookAdding.set_author)


dialog = Dialog(
    Window(
        Const("Перед вами открылось меню добавления новых книг!\n\n"
              "Чтобы продолжить, нажмите соответствующую кнопку, либо нажмите <b>Отмена</b>"),
        Row(
            SwitchTo(
                text=Const("Продолжить"),
                id="show_genres",
                state=BookAdding.set_genre
            ),
            Cancel(Const("Отмена"), on_click=on_cancel_click),
        ),
        state=BookAdding.show_menu,
    ),
    Window(
        Format("Выберите жанр книги (всего {count}):"),
        ScrollingGroup(
            Select(
                Format("{item.name}"),
                id="genres_select",
                item_id_getter=operator.attrgetter("id"),
                items="genres",
                on_click=on_genre_click
            ),
            id="genres_scrolling",
            height=5,
            width=1
        ),
        state=BookAdding.set_genre,
        getter=get_genres
    ),
    Window(
        Const("Теперь напишите название вашей книги:"),
        TextInput(id="genre_name", on_success=on_name_input),
        state=BookAdding.set_name
    )
)
