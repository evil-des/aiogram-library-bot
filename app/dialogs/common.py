from aiogram_dialog.widgets.kbd import (
    Row, Button, Cancel, Back, Group, Next
)
from aiogram_dialog.widgets.text import Const, Text
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Window
from typing import List, Optional


class CommonElements:
    @staticmethod
    async def on_cancel_click(
            c: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ) -> None:
        await dialog_manager.reset_stack()
        await c.message.answer("Действие отменено!")
        await c.message.delete()

    @staticmethod
    async def on_input_error(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
    ) -> None:
        await message.answer("Вы ошиблись при вводе! Попробуйте еще раз")

    @staticmethod
    def back_btn() -> Back:
        return Back(Const("🔙 Назад"))

    @staticmethod
    def cancel_btn() -> Cancel:
        return Cancel(
            Const("❌ Отмена"),
            id="cancel",
            on_click=CommonElements.on_cancel_click
        )

    @staticmethod
    def back_n_cancel() -> Row:
        return Row(
            CommonElements.back_btn(),
            CommonElements.cancel_btn()
        )

    @staticmethod
    def delete_btn(on_click) -> Button:
        return Button(
            Const("❌ Удалить"),
            id="delete",
            on_click=on_click
        )

    @staticmethod
    def input(
            id: str,
            text: Text,
            state,
            on_success=None,
            on_error=None,
            type_factory=str,
            filter=None,
            buttons: Optional[List[Button]] = None,
            skip=False
    ) -> Window:
        if on_error is None:
            on_error = CommonElements.on_input_error

        base = (
            text,
            TextInput(id=id, on_success=on_success, on_error=on_error,
                      filter=filter, type_factory=type_factory),
            CommonElements.back_n_cancel()
        )
        skip_btn = Next(Const("Пропустить"))

        if skip and buttons is not None:
            buttons = Group(*buttons, width=2)
            return Window(*base, buttons, skip_btn, state=state)
        elif skip:
            return Window(*base, skip_btn, state=state)

        if buttons is not None:
            buttons = Group(*buttons, width=2)
            return Window(*base, buttons, state=state)

        return Window(*base, state=state)
