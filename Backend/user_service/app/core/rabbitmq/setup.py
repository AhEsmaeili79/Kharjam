"""RabbitMQ setup and configuration"""
import logging
from .connection import get_rabbitmq_connection
from app.config import rabbitmq_config

logger = logging.getLogger(__name__)


def setup_rabbitmq() -> None:
    """Setup RabbitMQ exchanges and queues"""
    try:
        conn = get_rabbitmq_connection()
        if not conn.is_connected():
            conn.connect()
        channel = conn.channel

        if not channel:
            raise Exception("Failed to get RabbitMQ channel")

        # Declare exchanges
        channel.exchange_declare(
            exchange=rabbitmq_config.otp_exchange,
            exchange_type=rabbitmq_config.exchange_type,
            durable=True,
            auto_delete=False
        )
        channel.exchange_declare(
            exchange=rabbitmq_config.user_lookup_exchange,
            exchange_type=rabbitmq_config.exchange_type,
            durable=True,
            auto_delete=False
        )
        # Direct exchange for batched user info RPC
        channel.exchange_declare(
            exchange=rabbitmq_config.user_info_exchange,
            exchange_type=rabbitmq_config.user_info_exchange_type,
            durable=True,
            auto_delete=False
        )

        # Declare queues
        queues = [
            rabbitmq_config.email_queue,
            rabbitmq_config.sms_queue,
            rabbitmq_config.user_lookup_request_queue,
            rabbitmq_config.user_lookup_response_queue,
            rabbitmq_config.user_info_request_queue,
        ]
        for queue in queues:
            channel.queue_declare(
                queue=queue,
                durable=True,
                exclusive=False,
                auto_delete=False,
                arguments={"x-message-ttl": rabbitmq_config.message_ttl},
            )

        # Bind queues
        channel.queue_bind(
            exchange=rabbitmq_config.otp_exchange,
            queue=rabbitmq_config.email_queue,
            routing_key=rabbitmq_config.email_routing_key
        )
        channel.queue_bind(
            exchange=rabbitmq_config.otp_exchange,
            queue=rabbitmq_config.sms_queue,
            routing_key=rabbitmq_config.sms_routing_key
        )
        channel.queue_bind(
            exchange=rabbitmq_config.user_lookup_exchange,
            queue=rabbitmq_config.user_lookup_request_queue,
            routing_key=rabbitmq_config.user_lookup_request_key
        )
        channel.queue_bind(
            exchange=rabbitmq_config.user_lookup_exchange,
            queue=rabbitmq_config.user_lookup_response_queue,
            routing_key=rabbitmq_config.user_lookup_response_key
        )

        # Bind user info RPC queue (direct exchange)
        channel.queue_bind(
            exchange=rabbitmq_config.user_info_exchange,
            queue=rabbitmq_config.user_info_request_queue,
            routing_key=rabbitmq_config.user_info_request_routing_key,
        )

        logger.info("RabbitMQ setup completed successfully")
    except Exception as e:
        logger.error(f"Failed to setup RabbitMQ: {e}")
        logger.warning("Application will continue without RabbitMQ functionality")


def init_rabbitmq() -> None:
    """Initialize RabbitMQ"""
    logger.info("Starting RabbitMQ initialization...")
    try:
        setup_rabbitmq()
    except Exception as e:
        logger.error(f"Failed to setup RabbitMQ: {e}")
        logger.warning("Application will continue without RabbitMQ functionality")

