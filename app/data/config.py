from secrets import token_hex
from typing import Optional, Dict, Any, List

from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn, validator, RedisDsn


class DefaultSettings(BaseSettings):
    VERSION: str = "1.0.0"

    DEBUG: bool = Field(default=False)
    LOGGING_LEVEL: int = Field(default=10)

    USE_WEBHOOK: bool = Field(default=False)

    if USE_WEBHOOK:
        MAIN_WEBHOOK_ADDRESS: Optional[str] = Field(default=None)
        MAIN_WEBHOOK_SECRET_TOKEN: Optional[str] = Field(default=None)

        MAIN_WEBHOOK_LISTENING_HOST: Optional[str] = Field(default=None)
        MAIN_WEBHOOK_LISTENING_PORT: Optional[int] = Field(default=None)

        MAX_UPDATES_IN_QUEUE: Optional[int] = Field(default=None)

    USE_CUSTOM_API_SERVER: bool = Field(default=False)

    if USE_CUSTOM_API_SERVER:
        CUSTOM_API_SERVER_IS_LOCAL: Optional[bool] = Field(default=False)
        CUSTOM_API_SERVER_BASE: Optional[str] = Field(default=None)
        CUSTOM_API_SERVER_FILE: Optional[str] = Field(default=None)

    POSTGRES_USER: str = Field(default="user")
    POSTGRES_PASSWORD: str = Field(default="postgres_password")
    POSTGRES_DB: str = Field(default="database")
    POSTGRES_HOST: str = Field(default="127.0.0.1")
    POSTGRES_PORT: int = Field(default="5432")

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f'{values.get("POSTGRES_DB") or ""}',
            port=values.get("POSTGRES_PORT") or None,
        )

    BOT_TOKEN: str = Field(default="need_token")

    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: str = Field(default="redis_password")

    REDIS_CACHE_DB: int = Field(default=5)
    REDIS_STORAGE_DB: int = Field(default=3)

    REDIS_URI: Optional[RedisDsn] = None

    @validator("REDIS_URI", pre=True)
    def assemble_redis_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_HOST"),
            port=values.get("REDIS_PORT"),
            password=values.get("REDIS_PASSWORD"),
            path="/1",
        )
