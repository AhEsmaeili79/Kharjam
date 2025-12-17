"""User domain model"""
import enum
import uuid
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.sql import func
from app.db import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    user = "user"
    group_admin = "group_admin"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String(100), nullable=True, index=True)
    phone_number = Column(String(15), unique=True, nullable=True, index=True)
    avatar_url = Column(String, nullable=True)
    card_number = Column(String, nullable=True)
    card_holder_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    email = Column(String(255), unique=True, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

