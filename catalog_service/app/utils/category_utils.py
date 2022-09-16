from fastapi_cache import FastAPICache
from app.core.config import settings

async def clear_category_cache():
	await FastAPICache.get_backend().clear(namespace=settings.category_namespace)
