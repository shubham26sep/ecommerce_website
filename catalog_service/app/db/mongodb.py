# import logging
from motor.motor_asyncio import AsyncIOMotorClient

# log = logging.getLogger(__name__)
from loguru import logger


class Database:
    client: AsyncIOMotorClient = None


db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_database():
    logger.info("Connecting to MongoDB.")
    print('testing')
    # TODO: Move db settings to config
    path = 'mongodb://localhost:27017'
    db.client = AsyncIOMotorClient(path,
                                   maxPoolSize=3,
                                   minPoolSize=1)
    logger.info("Connected to MongoDB.")


async def close_mongo_connection():
    logger.info("Closing database connection..." )
    db.client.close()
    logger.info("Database connection closed!")
