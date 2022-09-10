from bson import ObjectId
from typing import Optional
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
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


class CategoryInModel(BaseModel):
    name: str
    parent: Optional[str]
