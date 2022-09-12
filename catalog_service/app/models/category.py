from bson import ObjectId
from typing import List, Optional
from pydantic import BaseModel, Field

from app.db.mongodb import PyObjectId

class CategoryModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    parent: str
    level: int
    path: str

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


class CategoryInModel(BaseModel):
    name: str
    parent: Optional[str]


class CategoryListModel(CategoryModel):
    subcategories: Optional[List['CategoryModel']]

class CategoryListResponseSchema(BaseModel):
    categories: List[CategoryListModel]
