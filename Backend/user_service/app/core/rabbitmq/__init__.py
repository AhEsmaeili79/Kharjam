"""RabbitMQ module"""
from .connection import get_rabbitmq_connection
from .producer import get_rabbitmq_producer, RabbitMQProducer
from .consumer import get_rabbitmq_consumer, create_user_lookup_callback
from .setup import init_rabbitmq, setup_rabbitmq
from app.tasks.user_lookup_consumer import (
    get_user_lookup_consumer_manager,
    start_user_lookup_consumer,
    stop_user_lookup_consumer,
    UserLookupConsumer,
)
from app.tasks.user_info_consumer import (
    UserInfoConsumer,
    get_user_info_consumer_manager,
    start_user_info_consumer,
    stop_user_info_consumer,
)

__all__ = [
    "get_rabbitmq_connection",
    "get_rabbitmq_producer",
    "RabbitMQProducer",
    "get_rabbitmq_consumer",
    "create_user_lookup_callback",
    "init_rabbitmq",
    "setup_rabbitmq",
    "get_user_lookup_consumer_manager",
    "start_user_lookup_consumer",
    "stop_user_lookup_consumer",
    "UserLookupConsumer",
    "UserInfoConsumer",
    "get_user_info_consumer_manager",
    "start_user_info_consumer",
    "stop_user_info_consumer",
]

