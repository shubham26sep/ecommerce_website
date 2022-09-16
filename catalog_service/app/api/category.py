from loguru import logger
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.exceptions import HTTPException
from fastapi_cache.decorator import cache

from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models import SuccessResponseSchema, ErrorResponseSchema
from app.models.category import CategoryInModel, CategoryListResponseSchema, CategoryModel
from app.services.category import CategoryService

router = APIRouter(prefix="/catalogs/categories")

@router.post(
    "/", response_model=SuccessResponseSchema
)
async def create_category(
    category: CategoryInModel,
    # user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
    ):
    logger.info(category)
    try:
        category = await CategoryService().create_category(category.dict())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail=jsonable_encoder(ErrorResponseSchema(statusCode=400, message = str(e))))
    return SuccessResponseSchema(data=category)


@router.get(
    "/", response_model=SuccessResponseSchema
)
@cache(expire=3600)
async def category_list(
    # user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
    ):
    try:
        categories = await CategoryService().category_list()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail=jsonable_encoder(ErrorResponseSchema(statusCode=400, message = str(e))))
    return SuccessResponseSchema(data=CategoryListResponseSchema(categories=categories))


@router.patch(
    "/{category_id}", response_model=SuccessResponseSchema
)
async def update_category(
    category_id: str,
    category: CategoryInModel,
    # user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
    ):
    logger.info(category)
    try:
        category = await CategoryService().update_category(category_id, category.dict(exclude_unset=True))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail=jsonable_encoder(ErrorResponseSchema(statusCode=400, message = str(e))))
    return SuccessResponseSchema(data=category)
