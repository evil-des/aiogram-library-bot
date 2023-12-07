from .base import BaseListingWindow
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager
from app.services.repo import Repo
from app.models import Genre
from app.dialogs.common import CommonElements
from typing import List, Any, Optional


class GenresWindow(BaseListingWindow):
    LISTING_MESSAGE = "Выберите жанр книги (всего {count} шт.):"
    HEIGHT = 3

    def __init__(self, state: State, switch_to: Optional[State] = None):
        super().__init__(
            id="genres",
            state=state,
            elements=[CommonElements.cancel_btn()],
            switch_to=switch_to
        )

    def data_getter(self, **kwargs):
        async def get_data(dialog_manager: DialogManager, **kwargs):
            repo: Repo = dialog_manager.middleware_data["repo"]
            genres: List[Genre] = await repo.genre_dao.get_genres()

            return {
                "items": genres,
                "count": len(genres)
            }
        return get_data
