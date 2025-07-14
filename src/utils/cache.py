import redis
import json
import asyncio
from typing import Any, Optional, Callable
import os

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', '6379')),
            decode_responses=True
        )

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            cached = self.redis_client.get(key)
            if cached:
                return json.loads(cached)
            return None
        except Exception:
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        try:
            self.redis_client.setex(key, ttl, json.dumps(value))
            return True
        except Exception:
            return False

    async def get_or_compute(self, key: str, compute_func: Callable, ttl: int = 3600) -> Any:
        """Get from cache or compute and store"""
        # Check cache first
        cached = await self.get(key)
        if cached is not None:
            return cached
        
        # Compute value
        result = await compute_func()
        
        # Store in cache
        await self.set(key, result, ttl)
        
        return result

    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception:
            return False

    async def clear_pattern(self, pattern: str) -> bool:
        """Clear all keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception:
            return False
