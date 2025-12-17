"""User lookup consumer task"""
import logging
import threading
from typing import Optional
from app.core.rabbitmq import get_rabbitmq_consumer, create_user_lookup_callback
from app.config import rabbitmq_config
from app.apps.users.selectors import UserSelector
from app.db import SessionLocal
from app.core.rabbitmq import get_rabbitmq_producer
from datetime import datetime

logger = logging.getLogger(__name__)


class UserLookupConsumer:
    """User lookup consumer manager"""

    def __init__(self):
        self.consumer = get_rabbitmq_consumer()
        self.thread: Optional[threading.Thread] = None
        self.running = False

    def start(self):
        """Start consumer"""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True, name="UserLookupConsumer")
        self.thread.start()
        logger.info("🚀 User lookup consumer started")

    def stop(self):
        """Stop consumer"""
        if not self.running:
            return
        self.running = False
        self.consumer.stop_consuming()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        self.consumer.disconnect()
        logger.info("🛑 User lookup consumer stopped")

    def _run(self):
        """Run consumer loop"""
        try:
            callback = create_user_lookup_callback(self._handle)
            self.consumer.setup_consumer(rabbitmq_config.user_lookup_request_queue, callback)
            while self.running:
                try:
                    self.consumer.start_consuming()
                except Exception as e:
                    if self.running:
                        logger.error(f"Consumer error: {e}")
                        import time
                        time.sleep(5)
        except Exception as e:
            logger.error(f"Fatal error: {e}")
        finally:
            self.running = False

    def _handle(self, data: dict) -> bool:
        """Handle user lookup message"""
        try:
            request_id = data.get("request_id", "")
            phone_or_email = data.get("phone_or_email", "")
            group_slug = data.get("group_slug", "")

            # Lookup user
            with SessionLocal() as db:
                user = UserSelector.get_by_identifier(db, phone_or_email)
                user_data = None
                if user:
                    user_data = {
                        "user_id": user.id,
                        "name": user.name,
                        "phone_number": user.phone_number,
                        "email": user.email,
                        "role": user.role.value,
                        "avatar_url": user.avatar_url,
                        "card_number": user.card_number,
                        "card_holder_name": user.card_holder_name,
                        "created_at": user.created_at.isoformat() if user.created_at else None,
                        "updated_at": user.updated_at.isoformat() if user.updated_at else None
                    }

            # Publish response
            response = {
                "request_id": request_id,
                "success": bool(user_data),
                "user_data": user_data,
                "error_message": None if user_data else f"User not found: {phone_or_email}",
                "timestamp": datetime.utcnow().isoformat()
            }

            producer = get_rabbitmq_producer()
            return producer.publish_message(
                exchange=rabbitmq_config.user_lookup_exchange,
                routing_key=rabbitmq_config.user_lookup_response_key,
                message=response,
                correlation_id=request_id
            )
        except Exception as e:
            logger.error(f"Handle error: {e}")
            return False


# Singleton
_consumer_manager: Optional[UserLookupConsumer] = None


def get_consumer_manager() -> UserLookupConsumer:
    """Get singleton consumer manager"""
    global _consumer_manager
    if _consumer_manager is None:
        _consumer_manager = UserLookupConsumer()
    return _consumer_manager


def start_consumer():
    """Start consumer"""
    get_consumer_manager().start()


def stop_consumer():
    """Stop consumer"""
    get_consumer_manager().stop()

