"""RabbitMQ module"""
from .connection import get_rabbitmq_connection
from .producer import get_rabbitmq_producer, RabbitMQProducer
from .setup import init_rabbitmq, setup_rabbitmq

__all__ = [
    "get_rabbitmq_connection",
    "get_rabbitmq_producer",
    "RabbitMQProducer",
    "init_rabbitmq",
    "setup_rabbitmq",
]

