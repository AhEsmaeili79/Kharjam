from datetime import datetime

import pytest

from app.apps.auth.models import BlacklistedToken
from app.apps.auth.services import JWTService
from app.apps.users.models import User, UserRole


def test_request_otp_creates_user_and_sends_message(
    client,
    db_session,
    fake_cache,
    fake_producer,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        "app.apps.auth.services.otp_service.OTPService.generate_otp_code",
        staticmethod(lambda length=5: "12345"),
    )

    response = client.post("/auth/request-otp", json={"identifier": "+1234567890"})
    assert response.status_code == 200
    data = response.json()

    created_user = db_session.query(User).filter_by(phone_number="981234567890").first()
    assert created_user is not None
    assert data["otp_code"] == "12345"
    assert fake_cache.get(f"otp:{created_user.id}")["code"] == "12345"
    assert fake_producer.otp_messages[-1]["routing_key"] is not None


def test_verify_otp_returns_tokens(client, db_session, fake_cache):
    user = User(
        name="Test User",
        email="test@example.com",
        phone_number="981234567890",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    fake_cache.set(
        f"otp:{user.id}",
        {
            "code": "12345",
            "created_at": datetime.utcnow().isoformat(),
            "is_used": False,
        },
    )

    response = client.post(
        "/auth/verify-otp",
        json={"identifier": user.email, "otp_code": "12345"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["is_new_user"] is False


def test_verify_otp_rejects_invalid_code(client, db_session, fake_cache):
    user = User(
        name="Another",
        email="another@example.com",
        phone_number="981111111111",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    fake_cache.set(
        f"otp:{user.id}",
        {
            "code": "99999",
            "created_at": datetime.utcnow().isoformat(),
            "is_used": False,
        },
    )

    response = client.post(
        "/auth/verify-otp",
        json={"identifier": user.email, "otp_code": "12345"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired OTP"


def test_refresh_token_returns_new_tokens(client, db_session):
    user = User(
        name="Refresher",
        email="refresh@example.com",
        phone_number="982222222222",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    refresh_token = JWTService.create_refresh_token({"user_id": user.id})
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_token_rejects_blacklisted(client, db_session, fake_cache):
    user = User(
        name="Blacklisted",
        email="black@example.com",
        phone_number="983333333333",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    refresh_token = JWTService.create_refresh_token({"user_id": user.id})
    fake_cache.set(f"blacklist:{refresh_token}", "blacklisted")

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 401
    assert response.json()["detail"] == "Token blacklisted"


def test_logout_blacklists_refresh_token(client, db_session, fake_cache):
    user = User(
        name="Logout",
        email="logout@example.com",
        phone_number="984444444444",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    refresh_token = JWTService.create_refresh_token({"user_id": user.id})
    response = client.post("/auth/logout", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    assert response.json()["msg"] == "Logged out successfully"
    assert fake_cache.exists(f"blacklist:{refresh_token}")
    assert (
        db_session.query(BlacklistedToken)
        .filter_by(token=refresh_token, user_id=user.id)
        .first()
        is not None
    )


def test_check_user_validates_token(client, db_session):
    user = User(
        name="Checker",
        email="check@example.com",
        phone_number="985555555555",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    access_token = JWTService.create_access_token({"user_id": user.id})
    response = client.post(
        "/auth/check-user", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["msg"] == "Token is valid"

