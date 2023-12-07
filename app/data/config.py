from typing import Any, Optional

from pydantic import Field, field_validator, PostgresDsn, RedisDsn, ValidationInfo
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    VERSION: str = "1.0.0"

    DEBUG: bool = Field(default=False)
    LOGGING_LEVEL: int = Field(
        default=20
    )  # read here - https://docs.python.org/3/library/logging.html#levels

    @field_validator("LOGGING_LEVEL", mode="before")
    def set_logging_leve(cls, v: Optional[int], info: ValidationInfo):
        if info.data.get("DEBUG"):
            return 10

        if isinstance(v, int):
            return v

    USE_WEBHOOK: bool = Field(default=False)

    MAIN_WEBHOOK_ADDRESS: Optional[str] = Field(default=None)
    MAIN_WEBHOOK_SECRET_TOKEN: Optional[str] = Field(default=None)

    MAIN_WEBHOOK_LISTENING_HOST: Optional[str] = Field(default=None)
    MAIN_WEBHOOK_LISTENING_PORT: Optional[int] = Field(default=None)

    MAX_UPDATES_IN_QUEUE: Optional[int] = Field(default=None)

    USE_CUSTOM_API_SERVER: bool = Field(default=False)

    CUSTOM_API_SERVER_IS_LOCAL: Optional[bool] = Field(default=False)
    CUSTOM_API_SERVER_BASE: Optional[str] = Field(default=None)
    CUSTOM_API_SERVER_FILE: Optional[str] = Field(default=None)

    POSTGRES_USER: str = Field(default="user")
    POSTGRES_PASSWORD: str = Field(default="postgres_password")
    POSTGRES_DB: str = Field(default="database")
    POSTGRES_HOST: str = Field(default="127.0.0.1")
    POSTGRES_PORT: int = Field(default="5432")

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="after")
    def assemble_db(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            path=f'{info.data.get("POSTGRES_DB") or ""}',
            port=info.data.get("POSTGRES_PORT") or None,
        )

    BOT_TOKEN: str = Field(default="need_token")

    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: str = Field(default="redis_password")

    REDIS_CACHE_DB: int = Field(default=5)
    REDIS_STORAGE_DB: int = Field(default=3)

    REDIS_URI: Optional[RedisDsn] = None

    @field_validator("REDIS_URI", mode="after")
    def assemble_redis_uri(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=info.data.get("REDIS_HOST"),
            port=info.data.get("REDIS_PORT"),
            password=info.data.get("REDIS_PASSWORD"),
            path="/1",
        )
