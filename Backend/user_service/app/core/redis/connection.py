"""Redis connection management"""
import logging
from typing import Optional
import redis
from app.config import redis_config

logger = logging.getLogger(__name__)


class RedisConnection:
    """Redis connection manager"""

    def __init__(self):
        self.client: Optional[redis.Redis] = None

    def connect(self) -> bool:
        """Establish Redis connection"""
        try:
            self.client = redis.Redis(
                host=redis_config.host,
                port=redis_config.port,
                password=redis_config.password,
                db=redis_config.db,
                max_connections=redis_config.max_connections,
                socket_timeout=redis_config.socket_timeout,
                socket_connect_timeout=redis_config.socket_connect_timeout,
                decode_responses=True
            )
            self.client.ping()
            logger.info(f"Connected to Redis at {redis_config.host}:{redis_config.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if connection is active"""
        if self.client is None:
            return False
        try:
            self.client.ping()
            return True
        except Exception:
            return False

    def get_client(self) -> Optional[redis.Redis]:
        """Get Redis client"""
        if not self.is_connected():
            if not self.connect():
                return None
        return self.client


# Global connection instance
_redis_connection: Optional[RedisConnection] = None


def get_redis_connection() -> RedisConnection:
    """Get or create Redis connection"""
    global _redis_connection
    if _redis_connection is None or not _redis_connection.is_connected():
        _redis_connection = RedisConnection()
        _redis_connection.connect()
    return _redis_connection


def get_redis_client() -> Optional[redis.Redis]:
    """Get Redis client directly"""
    return get_redis_connection().get_client()

