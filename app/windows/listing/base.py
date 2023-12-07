import abc

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Text, Const
from typing import List, Any, Dict, Optional


class BaseListingWindow(Window):
    LISTING_MESSAGE: str = "Список объектов (всего {count} шт.):"
    BUTTON_TEXT: str = "{item.name}"

    def __init__(
            self,
            id: str,
            state: State
    ) -> None:
        objects = self.get_objects_keyboard(
            id=id,
            on_click=self.on_click(id),
            button_text=self.BUTTON_TEXT
        )
        super().__init__(
            Format(self.LISTING_MESSAGE),
            objects,
            getter=self.get_data,
            state=state
        )

    @staticmethod
    def get_objects_keyboard(
            id: str,
            on_click,
            button_text: str
    ) -> ScrollingGroup:
        genres = Select(
            Format(button_text),
            id=f"s_{id}",
            item_id_getter=lambda item: item.id,
            items="items",
            on_click=on_click
        )

        sg = ScrollingGroup(
            genres,
            id=id,
            height=5,
            width=1
        )

        return sg

    @staticmethod
    @abc.abstractmethod
    async def get_data(dialog_manager: DialogManager, **kwargs) -> Dict:
        """
        You must implement this method to get your own data
        :param dialog_manager: DialogManager
        :param kwargs:
        :return: you must return dict with required key "items" (that we iterate)
        """
        raise NotImplementedError

    def on_click(self, id: str):
        async def on_item_selected(
                callback: CallbackQuery,
                widget: Any,
                dialog_manager: DialogManager,
                item_id: str
        ) -> None:
            options = {f"{id}_obj_id": int(item_id)}
            dialog_manager.current_context().dialog_data.update(**options)
            await dialog_manager.next()

        return on_item_selected
