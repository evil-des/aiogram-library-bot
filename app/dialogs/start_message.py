from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from app.states.user import UserMainMenu

dialog = Dialog(
    Window(
        Format(
            "Приветствуем тебя, @{event.chat.username} ✌️\n\n"
            "Этот телеграмм-бот поможет тебе "
            "больше не держать названия любимых книг в голове :)\n\n"
            "Теперь ты можешь добавлять их в базу данных нашей библиотеки, "
            "а затем осуществлять удобный поиск по ней!"
        ),
        state=UserMainMenu.start,
    )
)
