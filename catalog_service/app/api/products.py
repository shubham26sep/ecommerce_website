from loguru import logger
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.exceptions import HTTPException
from fastapi_cache.decorator import cache

from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models import SuccessResponseSchema, ErrorResponseSchema
from app.models.products import ProductInModel
from app.services.products import ProductService


router = APIRouter(prefix="/catalogs/products")

@router.post(
    "/", response_model=SuccessResponseSchema
)
async def create_product(
    product: ProductInModel,
    # user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
    ):
    logger.info(product)
    try:
        product = await ProductService().create_product(product.dict())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail=jsonable_encoder(ErrorResponseSchema(statusCode=400, message = str(e))))
    return SuccessResponseSchema(data=product)
