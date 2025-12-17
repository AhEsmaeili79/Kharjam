"""User lookup consumer service"""
import logging
import threading
from typing import Optional
from datetime import datetime

from app.core.rabbitmq.consumer import get_rabbitmq_consumer, create_user_lookup_callback
from app.core.rabbitmq.producer import get_rabbitmq_producer
from app.config import rabbitmq_config
from app.apps.users.selectors import UserSelector
from app.db import SessionLocal

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
            logger.warning("User lookup consumer is already running")
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True, name="UserLookupConsumer")
        self.thread.start()
        logger.info("🚀 User lookup consumer started")

    def stop(self):
        """Stop consumer"""
        if not self.running:
            logger.warning("User lookup consumer is not running")
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
            logger.error(f"Fatal error in user lookup consumer: {e}")
        finally:
            self.running = False

    def _handle(self, data: dict) -> bool:
        """Handle user lookup message"""
        try:
            request_id = data.get("request_id", "")
            phone_or_email = data.get("phone_or_email", "")
            group_slug = data.get("group_slug", "")

            if not request_id:
                logger.error("Missing request_id in user lookup request")
                return False

            if not phone_or_email:
                logger.error("Missing phone_or_email in user lookup request")
                return False

            logger.info(f"Processing user lookup request: {request_id} for {phone_or_email}")

            # Lookup user
            user_data = None
            try:
                with SessionLocal() as db:
                    user = UserSelector.get_by_identifier(db, phone_or_email)
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
                        logger.info(f"User found: {user.id} for request {request_id}")
                    else:
                        logger.info(f"User not found for {phone_or_email} in request {request_id}")
            except Exception as db_error:
                logger.error(f"Database error during user lookup: {db_error}")
                return False

            # Publish response
            response = {
                "request_id": request_id,
                "success": bool(user_data),
                "user_data": user_data,
                "error_message": None if user_data else f"User not found: {phone_or_email}",
                "timestamp": datetime.utcnow().isoformat()
            }

            producer = get_rabbitmq_producer()
            success = producer.publish_message(
                exchange=rabbitmq_config.user_lookup_exchange,
                routing_key=rabbitmq_config.user_lookup_response_key,
                message=response,
                correlation_id=request_id
            )

            if success:
                logger.info(f"Response published successfully for request {request_id}")
            else:
                logger.error(f"Failed to publish response for request {request_id}")

            return success

        except Exception as e:
            logger.error(f"Error handling user lookup message: {e}", exc_info=True)
            return False


# Singleton
_consumer_manager: Optional[UserLookupConsumer] = None


def get_user_lookup_consumer_manager() -> UserLookupConsumer:
    """Get singleton consumer manager"""
    global _consumer_manager
    if _consumer_manager is None:
        _consumer_manager = UserLookupConsumer()
    return _consumer_manager


def start_user_lookup_consumer():
    """Start user lookup consumer"""
    get_user_lookup_consumer_manager().start()


def stop_user_lookup_consumer():
    """Stop user lookup consumer"""
    get_user_lookup_consumer_manager().stop()

