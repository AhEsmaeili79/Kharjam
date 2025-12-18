import json
from datetime import datetime
from types import SimpleNamespace

from app.tasks.user_info_consumer import UserInfoConsumer


class DummyChannel:
    def __init__(self):
        self.acked = []
        self.nacked = []

    def basic_ack(self, delivery_tag):
        self.acked.append(delivery_tag)

    def basic_nack(self, delivery_tag, requeue=False):
        self.nacked.append((delivery_tag, requeue))


def test_user_info_consumer_handle_empty_ids(monkeypatch):
    """Consumer should handle empty user_ids list and still publish a response."""

    # Arrange
    consumer = UserInfoConsumer()
    published = {}

    class DummyProducer:
        def publish_message(self, exchange, routing_key, message, correlation_id=None):
            published["exchange"] = exchange
            published["routing_key"] = routing_key
            published["message"] = message
            published["correlation_id"] = correlation_id
            return True

    from app.core import rabbitmq as rmq_module

    monkeypatch.setattr(
        rmq_module, "get_rabbitmq_producer", lambda: DummyProducer()
    )

    body = {
        "request_id": "req-1",
        "group_id": "group-1",
        "user_ids": [],
    }
    properties = SimpleNamespace(reply_to="reply_queue", correlation_id="corr-1")

    # Act
    ok = consumer._handle(body, properties)

    # Assert
    assert ok is True
    assert published["routing_key"] == "reply_queue"
    assert published["message"]["request_id"] == "req-1"
    assert published["message"]["group_id"] == "group-1"
    assert isinstance(
        datetime.fromisoformat(published["message"]["timestamp"]), datetime
    )

