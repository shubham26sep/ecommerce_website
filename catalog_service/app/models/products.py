from bson import ObjectId
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

from app.db.mongodb import PyObjectId


class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str]
    brand: str
    categories: dict
    prices: dict

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Men",
                "parent": "/",
                "level": 0,
                "path": "/Men"
            }
        }


class ImageInModel(BaseModel):
    image_url: HttpUrl


class ProductInModel(BaseModel):
    title: str
    description: Optional[str]
    brand: str
    category_id: str
    image_url: Optional[List[ImageInModel]]
    price: float
