from app.services.dao.author import AuthorDAO
from app.services.dao.book import BookDAO
from app.services.dao.genre import GenreDAO
from app.services.dao.user import UserDAO

__all__ = [
    "UserDAO",
    "GenreDAO",
    "AuthorDAO",
    "BookDAO",
]
