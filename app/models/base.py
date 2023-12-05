import typing
import uuid

import orjson
import pydantic
from sqlmodel import SQLModel, Field


def orjson_dumps(
    v: typing.Any,
    *,
    default: typing.Optional[typing.Callable[[typing.Any], typing.Any]],
) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseModel(pydantic.BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

        json_encoders = {uuid.UUID: lambda x: f"{x}"}


class UserBase(SQLModel):
    full_name: str
    username: typing.Optional[str]


class BookBase(SQLModel):
    name: str
    author: str
    desc: str = Field(default="Описание книги не указано")


class GenreBase(SQLModel):
    name: str
    desc: str = Field(default="Описание жанра отсутствует")


class AuthorBase(SQLModel):
    full_name: str  # потому что некоторые авторы могут иметь отчество, а другие нет
