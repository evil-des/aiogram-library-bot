from datetime import datetime
from typing import List, Optional

from sqlmodel import BigInteger, Column, Field, Relationship, SQLModel

from .base import AuthorBase, BookBase, GenreBase, UserBase


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(sa_column=Column(BigInteger(), unique=True))
    join_date: datetime = Field(default=datetime.now())
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(
        back_populates="author", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Genre(GenreBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(
        back_populates="genre", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "selectin"}
    )

    genre_id: int = Field(default=None, foreign_key="genre.id")
    genre: Genre = Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "selectin"}
    )

    author_id: int = Field(default=None, foreign_key="author.id")
    author: Author = Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "selectin"}
    )


class BookAdd(BookBase):
    genre_id: int = Field(default=None)
    genre: str = Field(default=None)
    author: str = Field(default=None)


class BookFilter(SQLModel):
    IS_GENRE_FILTER: bool = False
    IS_KEY_WORD_FILTER: bool = False
