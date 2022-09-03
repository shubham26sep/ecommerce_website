from typing import Any, Optional
from pydantic import BaseModel


class SuccessResponseSchema(BaseModel):
    data: Optional[Any]
    message: Optional[str]
    success: Optional[bool]=True

class ErrorResponseSchema(BaseModel):
    statusCode: int
    message : Optional[str] = None
    success: Optional[bool]=False
