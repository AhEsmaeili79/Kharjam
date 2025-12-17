"""Token blacklist service"""
from app.core.redis import get_cache


class TokenBlacklistService:
    """Token blacklist service using Redis"""

    @staticmethod
    def blacklist_token(token: str, expires_in: int = 3600) -> bool:
        """Add token to blacklist"""
        key = f"blacklist:{token}"
        return get_cache().set(key, "blacklisted", expire=expires_in)

    @staticmethod
    def is_blacklisted(token: str) -> bool:
        """Check if token is blacklisted"""
        key = f"blacklist:{token}"
        return get_cache().exists(key)

