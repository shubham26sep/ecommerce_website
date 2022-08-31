from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.core.settings.app import AppSettings
from app.db.mongodb import connect_to_database, close_mongo_connection


def create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_database(app, settings)

    return start_app


def create_stop_app_handler() -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        await close_mongo_connection()

    return stop_app
