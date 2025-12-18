"""Batched user info consumer service"""
import json
import logging
import threading
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.rabbitmq.consumer import RabbitMQConsumer
from app.core.rabbitmq.consumer import get_rabbitmq_consumer
from app.core.rabbitmq.producer import get_rabbitmq_producer
from app.config import rabbitmq_config
from app.db import SessionLocal
from app.apps.users.models.user import User


logger = logging.getLogger(__name__)


class UserInfoConsumer:
    """Consumer that handles batched user info lookup requests.

    Expected message body:
        {
            "request_id": str,
            "group_id": str,
            "user_ids": [str, ...]
        }
    """

    def __init__(self) -> None:
        self.consumer: RabbitMQConsumer = get_rabbitmq_consumer()
        self.thread: Optional[threading.Thread] = None
        self.running: bool = False

    def start(self) -> None:
        """Start the consumer in a background thread."""
        if self.running:
            logger.warning("User info consumer is already running")
            return

        self.running = True
        self.thread = threading.Thread(
            target=self._run, daemon=True, name="UserInfoConsumer"
        )
        self.thread.start()
        logger.info("🚀 User info consumer started")

    def stop(self) -> None:
        """Stop the consumer and join the thread."""
        if not self.running:
            logger.warning("User info consumer is not running")
            return

        self.running = False
        self.consumer.stop_consuming()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        self.consumer.disconnect()
        logger.info("🛑 User info consumer stopped")

    def _run(self) -> None:
        """Run the consumer loop."""
        try:
            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body.decode("utf-8"))
                except json.JSONDecodeError as e:
                    logger.error(f"❌ JSON decode error in user info consumer: {e}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    return

                try:
                    success = self._handle(data, properties)
                except Exception as e:
                    logger.error(
                        f"💥 Error handling user info message: {e}", exc_info=True
                    )
                    success = False

                if success:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    # Requeue to allow transient issues to be retried
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            self.consumer.setup_consumer(
                rabbitmq_config.user_info_request_queue, callback
            )

            while self.running:
                try:
                    self.consumer.start_consuming()
                except Exception as e:
                    if self.running:
                        logger.error(f"User info consumer error: {e}", exc_info=True)
                        import time

                        time.sleep(5)
        except Exception as e:
            logger.error(f"Fatal error in user info consumer: {e}", exc_info=True)
        finally:
            self.running = False

    def _handle(self, data: Dict[str, Any], properties) -> bool:
        """Handle a single batched user info request."""
        request_id = data.get("request_id") or ""
        group_id = data.get("group_id") or ""
        user_ids: List[str] = data.get("user_ids") or []

        if not request_id:
            logger.error("Missing request_id in user info request")
            return False

        if not isinstance(user_ids, list) or not user_ids:
            logger.warning(
                f"Empty or invalid user_ids list for request_id={request_id}, group_id={group_id}"
            )

        reply_to = getattr(properties, "reply_to", None)
        correlation_id = getattr(properties, "correlation_id", None)

        if not reply_to:
            logger.error(
                f"Missing reply_to in message properties for request_id={request_id}"
            )
            return False

        logger.info(
            f"Processing batched user info request_id={request_id}, "
            f"group_id={group_id}, user_count={len(user_ids)}"
        )

        users_out: List[Dict[str, Any]] = []

        try:
            if user_ids:
                with SessionLocal() as db:
                    # Deduplicate user_ids for efficiency
                    unique_user_ids = list({uid for uid in user_ids if uid})
                    if unique_user_ids:
                        query = (
                            db.query(User)
                            .filter(User.id.in_(unique_user_ids))
                            .all()
                        )
                        for user in query:
                            users_out.append(
                                {
                                    "user_id": user.id,
                                    "name": user.name,
                                    "avatar_url": user.avatar_url,
                                    "card_number": user.card_number,
                                    "card_holder_name": user.card_holder_name,
                                    "created_at": user.created_at.isoformat()
                                    if user.created_at
                                    else None,
                                }
                            )
        except Exception as db_error:
            logger.error(
                f"Database error during batched user info lookup for request_id={request_id}: "
                f"{db_error}",
                exc_info=True,
            )
            return False

        response: Dict[str, Any] = {
            "request_id": request_id,
            "group_id": group_id,
            "users": users_out,
            "timestamp": datetime.utcnow().isoformat(),
        }

        producer = get_rabbitmq_producer()
        try:
            # Use default exchange to publish directly to the reply_to queue
            success = producer.publish_message(
                exchange="",
                routing_key=reply_to,
                message=response,
                correlation_id=correlation_id or request_id,
            )
        except Exception as e:
            logger.error(
                f"Failed to publish batched user info response for request_id={request_id}: {e}",
                exc_info=True,
            )
            return False

        if success:
            logger.info(
                f"Published batched user info response for request_id={request_id}, "
                f"returned_users={len(users_out)}"
            )
        else:
            logger.error(
                f"Failed to publish batched user info response for request_id={request_id}"
            )

        return success


# Singleton manager
_user_info_consumer_manager: Optional[UserInfoConsumer] = None


def get_user_info_consumer_manager() -> UserInfoConsumer:
    """Return singleton user info consumer manager."""
    global _user_info_consumer_manager
    if _user_info_consumer_manager is None:
        _user_info_consumer_manager = UserInfoConsumer()
    return _user_info_consumer_manager


def start_user_info_consumer() -> None:
    """Start the batched user info consumer."""
    get_user_info_consumer_manager().start()


def stop_user_info_consumer() -> None:
    """Stop the batched user info consumer."""
    get_user_info_consumer_manager().stop()


