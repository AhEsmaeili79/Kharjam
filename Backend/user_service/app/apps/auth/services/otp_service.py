"""OTP service"""
import random
import string
import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.core.redis import get_cache
from app.core.rabbitmq import get_rabbitmq_producer
from app.config import rabbitmq_config
from app.utils.validators import normalize_phone_number

logger = logging.getLogger(__name__)


class OTPService:
    """OTP service"""

    @staticmethod
    def generate_otp_code(length: int = 5) -> str:
        """Generate random OTP code"""
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def create_otp(user_id: str) -> Dict:
        """Create and cache OTP"""
        otp_code = OTPService.generate_otp_code()
        cache_key = f"otp:{user_id}"

        otp_data = {
            "code": otp_code,
            "created_at": datetime.utcnow().isoformat(),
            "is_used": False
        }

        cache = get_cache()
        success = cache.set(cache_key, otp_data, expire=600)  # 10 minutes

        if not success:
            logger.warning(f"Failed to store OTP in cache for user {user_id}")

        return {
            "user_id": user_id,
            "code": otp_code,
            "expires_in": 600,
            "cached": success
        }

    @staticmethod
    def validate_otp(user_id: str, otp_code: str) -> bool:
        """Validate OTP code"""
        cache_key = f"otp:{user_id}"
        cache = get_cache()
        otp_data = cache.get(cache_key)

        if not otp_data:
            return False

        if otp_data.get("is_used", False):
            return False

        if otp_data.get("code") != otp_code:
            return False

        # Check expiration
        created_at_str = otp_data.get("created_at")
        if created_at_str:
            try:
                created_at = datetime.fromisoformat(created_at_str)
                if datetime.utcnow() - created_at > timedelta(minutes=10):
                    cache.delete(cache_key)
                    return False
            except (ValueError, TypeError):
                cache.delete(cache_key)
                return False

        # OTP is valid, remove it
        cache.delete(cache_key)
        return True

    @staticmethod
    def get_identifier_type(identifier: str) -> str:
        """Determine if identifier is email or phone_number"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return "email" if re.match(email_pattern, identifier) else "phone_number"

    @staticmethod
    def send_otp_message(identifier: str, otp_code: str, identifier_type: str) -> bool:
        """Send OTP message via RabbitMQ"""
        try:
            producer = get_rabbitmq_producer()
            if not producer:
                logger.warning("RabbitMQ producer is not available")
                return False

            routing_key = (
                rabbitmq_config.email_routing_key
                if identifier_type == "email"
                else rabbitmq_config.sms_routing_key
            )

            return producer.publish_otp_message(identifier, otp_code, routing_key)
        except Exception as e:
            logger.warning(f"RabbitMQ connection error - OTP message not sent: {e}")
            return False

