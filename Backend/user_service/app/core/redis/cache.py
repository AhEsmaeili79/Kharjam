"""Redis cache service"""
import json
import logging
from typing import Any, Optional
from .connection import get_redis_client

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache service"""

    def __init__(self):
        self.client = get_redis_client()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if not self.client:
                return None
            value = self.client.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error getting cache key '{key}': {e}")
            return None

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in cache"""
        try:
            if not self.client:
                return False
            if not isinstance(value, str):
                value = json.dumps(value)
            return self.client.set(key, value, ex=expire) is True
        except Exception as e:
            logger.error(f"Error setting cache key '{key}': {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if not self.client:
                return False
            return self.client.delete(key) > 0
        except Exception as e:
            logger.error(f"Error deleting cache key '{key}': {e}")
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            if not self.client:
                return False
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking cache key '{key}': {e}")
            return False


# Global cache instance
_cache_instance: Optional[RedisCache] = None


def get_cache() -> RedisCache:
    """Get or create cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache()
    return _cache_instance

