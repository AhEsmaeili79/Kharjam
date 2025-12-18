"""RabbitMQ consumer service"""
import json
import logging
from typing import Callable, Optional
import pika
from .connection import get_rabbitmq_connection
from app.config import rabbitmq_config

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    """RabbitMQ consumer service"""

    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None

    def connect(self) -> None:
        """Establish connection"""
        conn = get_rabbitmq_connection()
        if not conn.is_connected():
            conn.connect()
        self.connection = conn.connection
        self.channel = conn.channel
        if self.channel:
            self.channel.basic_qos(prefetch_count=1)
        logger.info("RabbitMQ consumer connected")

    def setup_consumer(self, queue_name: str, callback: Callable) -> None:
        """Setup consumer for queue"""
        if not self.connection or self.connection.is_closed:
            self.connect()

        try:
            self.channel.queue_declare(
                queue=queue_name,
                durable=True,
                exclusive=False,
                auto_delete=False,
                arguments={'x-message-ttl': rabbitmq_config.message_ttl}
            )
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=False
            )
            logger.info(f"Consumer setup for queue: {queue_name}")
        except Exception as e:
            logger.error(f"Failed to setup consumer: {e}")
            raise

    def start_consuming(self) -> None:
        """Start consuming messages"""
        try:
            logger.info("Starting to consume messages...")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stop_consuming()
        except Exception as e:
            logger.error(f"Error while consuming: {e}")
            raise

    def stop_consuming(self) -> None:
        """Stop consuming messages"""
        if self.channel and not self.channel.is_closed:
            self.channel.stop_consuming()
        logger.info("Stopped consuming messages")

    def disconnect(self) -> None:
        """Disconnect consumer"""
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        logger.info("RabbitMQ consumer disconnected")


def create_user_lookup_callback(handler: Callable) -> Callable:
    """Create callback for user lookup messages"""
    def callback(ch, method, properties, body):
        try:
            data = json.loads(body.decode('utf-8'))
            request_id = data.get('request_id', 'UNKNOWN')
            logger.info(f"📨 Received message: {request_id}")
            success = handler(data)
            if success:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                logger.info(f"✅ Processed: {request_id}")
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                logger.warning(f"⚠️ Failed: {request_id}")
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"💥 Error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    return callback


def get_rabbitmq_consumer() -> RabbitMQConsumer:
    """Create a new RabbitMQ consumer instance.

    Note:
        We intentionally return a **new** `RabbitMQConsumer` on each call
        instead of sharing a global singleton. Each consumer manages its
        own `BlockingConnection`/channel, and we run multiple consumers
        in different threads. Sharing a single consumer (and thus a single
        connection/channel) across threads was leading to errors such as:

            - \"Stream connection lost: IndexError('pop from an empty deque')\"
            - \"start_consuming may not be called from the scope of another
              BlockingConnection or BlockingChannel callback\"

        By giving each high-level consumer manager its own `RabbitMQConsumer`,
        we avoid cross-thread interference and re-entrancy issues in Pika.
    """
    return RabbitMQConsumer()

