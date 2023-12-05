from app.db import async_session
from app.models import Genre
from sqlalchemy.exc import PendingRollbackError, IntegrityError


GENRES = [
    {"name": "Деловая литература"},
    {"name": "Детективы и Триллеры"},
    {"name": "Документальная литература"},
    {"name": "Дом, ремесла, досуг, хобби"},
    {"name": "Драматургия"},
    {"name": "Искусство, Искусствоведение, Дизайн"},
    {"name": "Компьютеры и Интернет"},
    {"name": "Литература для детей"},
    {"name": "Любовные романы"},
    {"name": "Наука, Образование"},
    {"name": "Поэзия"},
    {"name": "Приключения"},
    {"name": "Проза"},
    {"name": "Прочее"},
    {"name": "Религия, духовность, эзотерика"},
    {"name": "Справочная литература"},
    {"name": "Старинное"},
    {"name": "Техника"},
    {"name": "Учебники и пособия"},
    {"name": "Фантастика"},
    {"name": "Фольклор"},
    {"name": "Юмор"},
    {"name": "Здоровье, красота, психология"},
    {"name": "Зарубежная литература"}
]


async def prepare_data():
    async with async_session() as session:
        for genre in GENRES:
            db_genre = Genre(
                name=genre.get("name"),
                desc=genre.get("desc")
            )
            session.add(db_genre)

        try:
            await session.commit()
        except IntegrityError or PendingRollbackError:
            await session.rollback()
