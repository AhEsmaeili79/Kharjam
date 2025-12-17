"""Token data access layer"""
from typing import Optional
from sqlalchemy.orm import Session
from app.apps.auth.models import BlacklistedToken


class TokenSelector:
    """Token data access selector"""

    @staticmethod
    def is_blacklisted(db: Session, token: str) -> bool:
        """Check if token is blacklisted"""
        return db.query(BlacklistedToken).filter_by(token=token).first() is not None

    @staticmethod
    def blacklist(db: Session, user_id: str, token: str) -> BlacklistedToken:
        """Add token to blacklist"""
        blacklisted = BlacklistedToken(user_id=user_id, token=token)
        db.add(blacklisted)
        db.commit()
        db.refresh(blacklisted)
        return blacklisted

