import logging

from pydantic import SecretStr

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test FastAPI catalog application"

    # secret_key: SecretStr = SecretStr("test_secret")

    database_url: str
    max_pool_size: int = 3
    min_connection_count: int = 1

    logging_level: int = logging.DEBUG
