from loguru import logger
from fastapi import APIRouter, Depends

from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.category import CategoryCreate

router = APIRouter(prefix="/catalogs")

@router.get("/")
async def test():
    return {'Hello': 'World'}


# @router.get("/categories")
# async def create_category():
#     return {'Hello': 'World'}

@router.post(
    "/categories"
)
async def create_category(
    category: CategoryCreate,
    # user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database),
    ):
    logger.info(category)
    response = await db['Catalogs']['Category'].insert_one(category.dict())
    logger.info(response)
    return {'success': 'true'}
