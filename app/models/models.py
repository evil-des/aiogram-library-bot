from sqlmodel import (
    Field, Relationship, BigInteger, Column
)
from .base import (
    UserBase, AuthorBase, GenreBase, BookBase
)
from typing import Optional, List
from datetime import datetime


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(sa_column=Column(BigInteger(), unique=True))
    join_date: datetime = Field(default=datetime.now())
    books: List["Book"] = Relationship(back_populates="user")


class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="author")


class Genre(GenreBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="genre")


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="books")

    genre_id: int = Field(default=None, foreign_key="genre.id")
    genre: Genre = Relationship(back_populates="books")

    author_id: int = Field(default=None, foreign_key="author.id")
    author: Author = Relationship(back_populates="books")
