"""RabbitMQ module"""
from .connection import get_rabbitmq_connection
from .producer import get_rabbitmq_producer, RabbitMQProducer
from .consumer import get_rabbitmq_consumer, RabbitMQConsumer, create_user_lookup_callback
from .setup import init_rabbitmq, setup_rabbitmq

__all__ = [
    "get_rabbitmq_connection",
    "get_rabbitmq_producer",
    "RabbitMQProducer",
    "get_rabbitmq_consumer",
    "RabbitMQConsumer",
    "create_user_lookup_callback",
    "init_rabbitmq",
    "setup_rabbitmq",
]

