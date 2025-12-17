from datetime import datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException

from app.apps.auth.services import JWTService, OTPService, TokenBlacklistService
from app.apps.users.models import User, UserRole
from app.apps.users.schemas import UserUpdate
from app.apps.users.selectors import UserSelector
from app.apps.users.services import UserService
from app.config import jwt_config


def test_otp_service_create_and_validate(fake_cache):
    otp = OTPService.create_otp("user-1")
    assert otp["code"] == fake_cache.get("otp:user-1")["code"]

    is_valid = OTPService.validate_otp("user-1", otp["code"])
    assert is_valid is True
    assert fake_cache.get("otp:user-1") is None


def test_otp_service_rejects_expired(fake_cache):
    expired = {
        "code": "54321",
        "created_at": (datetime.utcnow() - timedelta(minutes=11)).isoformat(),
        "is_used": False,
    }
    fake_cache.set("otp:user-2", expired)

    assert OTPService.validate_otp("user-2", "54321") is False


def test_jwt_service_encodes_and_decodes():
    token = JWTService.create_access_token({"user_id": "abc"})
    decoded = JWTService.decode_access_token(token)
    assert decoded is not None
    assert decoded["user_id"] == "abc"


def test_jwt_service_returns_none_on_invalid_token():
    expired_token = jwt.encode(
        {"user_id": "abc", "exp": datetime.utcnow() - timedelta(minutes=1)},
        jwt_config.secret_key,
        algorithm=jwt_config.algorithm,
    )
    assert JWTService.decode_access_token(expired_token) is None


def test_token_blacklist_service_marks_and_checks(fake_cache):
    token = "token-123"
    assert TokenBlacklistService.is_blacklisted(token) is False
    TokenBlacklistService.blacklist_token(token, expires_in=5)
    assert TokenBlacklistService.is_blacklisted(token) is True


def test_user_service_applies_validations(db_session):
    user = User(
        name="Valid Name",
        email="user@example.com",
        phone_number="981234567890",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    update = UserUpdate(email="new@example.com", phone_number="+1234567890", name="New Name")
    updated_user = UserService.validate_and_update_user(user, update, db_session)
    db_session.commit()
    db_session.refresh(updated_user)

    assert updated_user.email == "new@example.com"
    assert updated_user.phone_number.startswith("98")
    assert updated_user.name == "New Name"


def test_user_service_rejects_duplicate_email(db_session):
    existing = User(
        name="Existing",
        email="existing@example.com",
        phone_number="981111111111",
        role=UserRole.user,
    )
    target = User(
        name="Target",
        email="target@example.com",
        phone_number="981222222222",
        role=UserRole.user,
    )
    db_session.add_all([existing, target])
    db_session.commit()
    db_session.refresh(target)

    with pytest.raises(HTTPException) as exc:
        UserService.validate_and_update_user(target, UserUpdate(email="existing@example.com"), db_session)
    assert exc.value.status_code == 400


def test_user_selector_fetches_by_email_and_phone(db_session):
    user = User(
        name="Selector",
        email="selector@example.com",
        phone_number="981333333333",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()

    by_email = UserSelector.get_by_identifier(db_session, "selector@example.com")
    by_phone = UserSelector.get_by_identifier(db_session, "+1333333333")

    assert by_email == user
    assert by_phone == user

