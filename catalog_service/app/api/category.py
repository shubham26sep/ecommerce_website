from loguru import logger
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.exceptions import HTTPException

from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models import SuccessResponseSchema, ErrorResponseSchema
from app.models.category import CategoryCreate
from app.services.category import CategoryCRUD

router = APIRouter(prefix="/catalogs/categories")

@router.get("/")
async def test():
    return {'Hello': 'World'}


# @router.get("/categories")
# async def create_category():
#     return {'Hello': 'World'}

@router.post(
    "/"
)
async def create_category(
    category: CategoryCreate,
    # user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
    ):
    logger.info(category)
    try:
        response = await CategoryCRUD().create(category.dict())
        logger.info(response)
    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail=jsonable_encoder(ErrorResponseSchema(statusCode=400, message = str(e))))
    return {'success': 'true'}
