"""Health check routes"""
import logging
from fastapi import APIRouter
from app.db import check_db_connection
from app.core.redis.connection import RedisConnection
from app.core.rabbitmq.connection import RabbitMQConnection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


def check_redis_connection() -> bool:
    """Check Redis connection health"""
    try:
        conn = RedisConnection()
        return conn.connect()
    except Exception as e:
        logger.debug(f"Redis health check failed: {e}")
        return False


def check_rabbitmq_connection() -> bool:
    """Check RabbitMQ connection health"""
    try:
        conn = RabbitMQConnection()
        conn.connect()
        is_connected = conn.is_connected()
        # Close test connection
        conn.disconnect()
        return is_connected
    except Exception as e:
        logger.debug(f"RabbitMQ health check failed: {e}")
        return False


@router.get("/", operation_id="healthCheckApi", include_in_schema=False)
def health_check():
    """Health check endpoint with detailed service status"""
    db_status = check_db_connection()
    redis_status = check_redis_connection()
    rabbitmq_status = check_rabbitmq_connection()
    
    # Overall status is ok if database is connected (critical service)
    # Other services are optional
    overall_status = "ok" if db_status else "error"
    
    return {
        "status": overall_status,
        "services": {
            "database": {
                "status": "healthy" if db_status else "unhealthy",
                "connected": db_status
            },
            "redis": {
                "status": "healthy" if redis_status else "unhealthy",
                "connected": redis_status
            },
            "rabbitmq": {
                "status": "healthy" if rabbitmq_status else "unhealthy",
                "connected": rabbitmq_status
            }
        }
    }

