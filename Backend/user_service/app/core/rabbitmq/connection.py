"""RabbitMQ connection management"""
import logging
import pika
from typing import Optional
from app.config import rabbitmq_config

logger = logging.getLogger(__name__)


class RabbitMQConnection:
    """RabbitMQ connection manager"""

    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None

    def connect(self) -> pika.BlockingConnection:
        """Create RabbitMQ connection"""
        try:
            credentials = pika.PlainCredentials(
                rabbitmq_config.username,
                rabbitmq_config.password
            )
            parameters = pika.ConnectionParameters(
                host=rabbitmq_config.host,
                port=rabbitmq_config.port,
                virtual_host=rabbitmq_config.virtual_host,
                credentials=credentials,
                heartbeat=rabbitmq_config.heartbeat,
                connection_attempts=rabbitmq_config.connection_attempts,
                retry_delay=rabbitmq_config.retry_delay
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logger.info(f"Connected to RabbitMQ at {rabbitmq_config.host}:{rabbitmq_config.port}")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def is_connected(self) -> bool:
        """Check if connection is active"""
        return (
            self.connection is not None
            and not self.connection.is_closed
            and self.channel is not None
            and not self.channel.is_closed
        )

    def disconnect(self) -> None:
        """Close RabbitMQ connection"""
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        logger.info("RabbitMQ connection closed")


def get_rabbitmq_connection() -> RabbitMQConnection:
    """Create a new RabbitMQ connection manager instance.

    Note:
        We intentionally return a **new** `RabbitMQConnection` on each call
        instead of sharing a global instance. Pika's `BlockingConnection`
        and channels are not thread-safe, and we run multiple consumers
        in different threads. Sharing a single underlying connection/channel
        across threads was causing errors like:

            - "Stream connection lost: IndexError('pop from an empty deque')"
            - `pika.exceptions.ChannelWrongStateError: Channel is closed.`

        By giving each consumer (and each producer invocation) its own
        connection manager instance, we avoid cross-thread interference.
        Callers remain responsible for invoking `connect()` before use.
    """
    return RabbitMQConnection()

