from loguru import logger
from fastapi import APIRouter

router = APIRouter(prefix="/catalogs")

@router.get("/")
async def test():
    return {'Hello': 'World'}
