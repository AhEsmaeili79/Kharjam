"""Blacklisted Token domain model"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base


class BlacklistedToken(Base):
    """Blacklisted Token model"""
    __tablename__ = "blacklisted_tokens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False, index=True)
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

