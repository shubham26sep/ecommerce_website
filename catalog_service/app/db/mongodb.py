# import logging

# log = logging.getLogger(__name__)
from loguru import logger
from fastapi import FastAPI
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings.app import AppSettings

class Database:
    client: AsyncIOMotorClient = None


db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_database(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to MongoDB.")
    path = settings.database_url
    db.client = AsyncIOMotorClient(path,
                                   maxPoolSize=settings.max_pool_size,
                                   minPoolSize=settings.min_pool_size)
    logger.info("Connected to MongoDB.")


async def close_mongo_connection():
    logger.info("Closing database connection..." )
    db.client.close()
    logger.info("Database connection closed!")
