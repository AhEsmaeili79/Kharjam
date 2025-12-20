"""User service"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.apps.users.models import User
from app.apps.users.schemas import UserUpdate
from app.apps.users.selectors import UserSelector
from app.utils.validators import FIELD_VALIDATORS, normalize_phone_number
from app.core.errors import UserError


class UserService:
    """User business logic service"""

    @staticmethod
    def validate_and_update_user(user: User, update: UserUpdate, db: Session) -> User:
        """Validate and update user"""
        updates = update.model_dump(exclude_unset=True)
        for field, value in updates.items():
            if value is None or value == "" or getattr(user, field) == value:
                continue

            # Validate field
            validator = FIELD_VALIDATORS.get(field)
            if validator:
                validator(value)

            # Uniqueness checks
            if field == "phone_number":
                normalized_phone = normalize_phone_number(value)
                existing_user = db.query(User).filter(
                    or_(
                        User.phone_number == normalized_phone,
                        User.phone_number == value
                    ),
                    User.id != user.id
                ).first()
                if existing_user:
                    raise HTTPException(status_code=400, detail=UserError.PHONE_ALREADY_REGISTERED)
                setattr(user, field, normalized_phone)
            elif field == "email":
                if db.query(User).filter(User.email == value, User.id != user.id).first():
                    raise HTTPException(status_code=400, detail=UserError.EMAIL_ALREADY_REGISTERED)
                setattr(user, field, value)
            else:
                setattr(user, field, value)

        return user

