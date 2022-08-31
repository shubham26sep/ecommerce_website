from typing import Optional
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    parent: Optional[str]
    path: str
