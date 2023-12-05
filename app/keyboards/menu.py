from .default.consts import DefaultConstructor
import aiogram


class Menu(DefaultConstructor):
    @staticmethod
    def main() -> aiogram.types.ReplyKeyboardMarkup:
        schema = [2, 1]
        buttons = [
            "📚 Все книги",
            "🔎 Поиск книг",
            "➕ Добавить"
        ]
        return Menu._create_kb(buttons, schema)
