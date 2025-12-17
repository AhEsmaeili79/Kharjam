"""RabbitMQ producer service"""
import json
import logging
import pika
from typing import Dict, Any, Optional
from datetime import datetime
from .connection import get_rabbitmq_connection
from app.config import rabbitmq_config

logger = logging.getLogger(__name__)


class RabbitMQProducer:
    """RabbitMQ producer service"""

    def publish_otp_message(self, identifier: str, otp_code: str, routing_key: str) -> bool:
        """Publish OTP message"""
        try:
            conn = get_rabbitmq_connection()
            if not conn.connection or conn.connection.is_closed:
                conn.connect()

            message_data = {
                "identifier": identifier,
                "otp_code": otp_code,
                "timestamp": datetime.utcnow().isoformat()
            }

            conn.channel.basic_publish(
                exchange=rabbitmq_config.otp_exchange,
                routing_key=routing_key,
                body=json.dumps(message_data),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            logger.info(f"Published OTP message to {routing_key}: {identifier}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish OTP message: {e}")
            return False

    def publish_message(self, exchange: str, routing_key: str, message: Dict[str, Any], correlation_id: Optional[str] = None) -> bool:
        """Publish generic message"""
        try:
            conn = get_rabbitmq_connection()
            if not conn.connection or conn.connection.is_closed:
                conn.connect()

            properties = pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
            if correlation_id:
                properties.correlation_id = correlation_id

            conn.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=properties
            )
            logger.info(f"Published message to {exchange} with key {routing_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            return False


# Global producer instance
_rabbitmq_producer: Optional[RabbitMQProducer] = None


def get_rabbitmq_producer() -> RabbitMQProducer:
    """Get or create RabbitMQ producer"""
    global _rabbitmq_producer
    if _rabbitmq_producer is None:
        _rabbitmq_producer = RabbitMQProducer()
    return _rabbitmq_producer

