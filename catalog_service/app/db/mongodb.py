import datetime
from loguru import logger
from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseConfig, BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.settings.app import AppSettings

class Database:
    client: AsyncIOMotorClient = None


db = Database()

def get_database() -> AsyncIOMotorClient:
    return db.client[settings.database_name]


async def connect_to_database(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to MongoDB.")
    path = settings.database_url
    db.client = AsyncIOMotorClient(path,
                                   maxPoolSize=settings.max_pool_size,
                                   minPoolSize=settings.min_pool_size)
    #TODO: Add mongodb test query
    logger.info("Connected to MongoDB.")


async def close_mongo_connection():
    logger.info("Closing database connection..." )
    db.client.close()
    logger.info("Database connection closed!")


class MongoModel(BaseModel):

  class Config(BaseConfig):
      allow_population_by_field_name = True
      json_encoders = {
          datetime: lambda dt: dt.isoformat(),
          ObjectId: lambda oid: str(oid),
      }

  @classmethod
  def from_mongo(cls, data: dict):
      """We must convert _id into "id". """
      if not data:
          return data
      id = data.pop('_id', None)
      return cls(**dict(data, id=id))

  def mongo(self, **kwargs):
      exclude_unset = kwargs.pop('exclude_unset', True)
      by_alias = kwargs.pop('by_alias', True)

      parsed = self.dict(
          exclude_unset=exclude_unset,
          by_alias=by_alias,
          **kwargs,
      )

      # Mongo uses `_id` as default key. We should stick to that as well.
      if '_id' not in parsed and 'id' in parsed:
          parsed['_id'] = parsed.pop('id')

      return parsed

  def to_dict(self, **kwargs):
      exclude_unset = kwargs.pop('exclude_unset', True)
      by_alias = kwargs.pop('by_alias', True)

      parsed = self.dict(
          exclude_unset=exclude_unset,
          by_alias=by_alias,
          **kwargs,
      )
      return parsed


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
