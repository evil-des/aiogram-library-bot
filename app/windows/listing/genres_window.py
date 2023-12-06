from .base import BaseListingWindow
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager
from app.services.repo import Repo
from app.models import Genre
from typing import List, Any


class GenresWindow(BaseListingWindow):
    LISTING_MESSAGE = "Выберите жанр книги (всего {count} шт.):"

    def __init__(self, state: State):
        super().__init__(id="genres", state=state)

    @staticmethod
    async def get_data(dialog_manager: DialogManager, **kwargs):
        repo: Repo = dialog_manager.middleware_data["repo"]
        genres: List[Genre] = await repo.genre_dao.get_genres()

        return {
            "items": genres,
            "count": len(genres)
        }
