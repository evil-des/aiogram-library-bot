"""Functions for app settings."""

from os import environ

from app.data.config import DefaultSettings


def get_settings() -> DefaultSettings:
    """Return actual settings for app."""
    env = environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()

    return DefaultSettings()
