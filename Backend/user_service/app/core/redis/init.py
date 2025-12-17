"""Redis initialization"""
import logging
from .connection import get_redis_connection

logger = logging.getLogger(__name__)


def init_redis() -> None:
    """Initialize Redis connection"""
    logger.info("Starting Redis initialization...")
    try:
        conn = get_redis_connection()
        if conn.is_connected():
            logger.info("Redis setup completed successfully")
        else:
            logger.error("Redis health check failed")
            logger.warning("Application will continue without Redis caching functionality")
    except Exception as e:
        logger.error(f"Failed to setup Redis: {e}")
        logger.warning("Application will continue without Redis caching functionality")

