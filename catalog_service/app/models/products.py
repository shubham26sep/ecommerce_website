import requests
from enum import Enum
from bson import ObjectId
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, validator

from app.db.mongodb import PyObjectId


class ProductSizeEnum(str, Enum):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    XLARGE = 'XL'
    XXLARGE = 'XLL'


class ProductVariantModel(BaseModel):
	size: ProductSizeEnum
	price: float
	quantity: int


class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str]
    brand: str
    categories: dict
    prices: dict
    is_visible: bool
    images: List[str]
    variants: List[ProductVariantModel]

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

    @validator('image_url')
    def validate_image_url(cls, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise ValueError('Invalid/Expired image url')
        return url


class ProductInModel(BaseModel):
    title: str
    description: Optional[str]
    brand: str
    category_id: str
    price: float
    is_visible: bool = True
    images: Optional[List[ImageInModel]]
    variants: Optional[List[ProductVariantModel]]
