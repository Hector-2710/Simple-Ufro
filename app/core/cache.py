from typing import Optional, Any
import redis.asyncio as redis
import json
from app.core.config import settings

class CacheManager:
    client: Optional[redis.Redis] = None

    @classmethod
    async def connect(cls):
        cls.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        await cls.client.ping()
        print("✅ Redis Connected")

    @classmethod
    async def close(cls):
        if cls.client:
            await cls.client.close()
            print("🛑 Redis Closed")

    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        if not cls.client:
            return None
        val = await cls.client.get(key)
        if val:
            return json.loads(val)
        return None

    @classmethod
    async def set(cls, key: str, value: Any, ttl: int = 300):
        if not cls.client:
            return
        await cls.client.set(key, json.dumps(value), ex=ttl)

    @classmethod
    async def check_rate_limit(cls, key: str, limit: int, window: int) -> bool:
        if not cls.client:
            return True
        
        current = await cls.client.incr(key)
        if current == 1:
            await cls.client.expire(key, window)
            
        return current <= limit

cache = CacheManager()
