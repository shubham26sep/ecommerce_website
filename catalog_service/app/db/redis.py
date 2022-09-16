from loguru import logger
from redis.asyncio import RedisCluster
from redis.asyncio.cluster import ClusterNode
from fastapi_cache import FastAPICache

from app.core.settings.app import AppSettings

async def connect_to_redis_cluster(settings: AppSettings) -> None:
    logger.info("Connecting to Redis Cluster.")
    startup_nodes = [ClusterNode(host, port) for host, port in settings.redis_nodes]
    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    FastAPICache.init(RedisBackend(rc), prefix="catalogs")
    #TODO: Add redis test query
    logger.info("Connected to Redis Cluster.")


from typing import Tuple

from redis.asyncio.client import Redis

from fastapi_cache.backends import Backend


class RedisBackend(Backend):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_with_ttl(self, key: str) -> Tuple[int, str]:
        async with self.redis.pipeline(transaction=False) as pipe:
            return await (pipe.ttl(key).get(key).execute())

    async def get(self, key) -> str:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        return await self.redis.set(key, value, ex=expire)

    async def clear(self, namespace: str = None, key: str = None) -> int:
        if namespace:
            lua = f"for i, name in ipairs(redis.call('KEYS', '*:{namespace}:*')) do redis.call('DEL', name); end"
            return await self.redis.eval(lua, numkeys=0)
        elif key:
            return await self.redis.delete(key)
