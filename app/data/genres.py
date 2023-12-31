from app.services.repo import Repo

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
    {"name": "Зарубежная литература"},
]


async def prepare_db_data(repo: Repo):
    for genre in GENRES:
        await repo.genre_dao.create_genre_if_not_exist(
            name=genre.get("name"), desc=genre.get("desc")
        )
