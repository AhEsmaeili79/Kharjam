"""User data access layer (Repository pattern)"""
from typing import Optional
from sqlalchemy.orm import Session
from app.apps.users.models import User
from app.utils.validators import normalize_phone_number, EMAIL_PATTERN


class UserSelector:
    """User data access selector"""

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_phone(db: Session, phone_number: str) -> Optional[User]:
        """Get user by phone number"""
        normalized_phone = normalize_phone_number(phone_number)
        # Only check normalized phone since we always normalize
        return db.query(User).filter(User.phone_number == normalized_phone).first()

    @staticmethod
    def get_by_identifier(db: Session, identifier: str) -> Optional[User]:
        """Get user by email or phone number"""
        is_email = EMAIL_PATTERN.match(identifier) is not None

        if is_email:
            return UserSelector.get_by_email(db, identifier)
        else:
            return UserSelector.get_by_phone(db, identifier)

    @staticmethod
    def create(db: Session, user_data: dict) -> User:
        """Create new user"""
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db: Session, user: User, update_data: dict) -> User:
        """Update user"""
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

