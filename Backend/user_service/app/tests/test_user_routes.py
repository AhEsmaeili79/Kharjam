from app.apps.users.models import User, UserRole
from app.core import dependencies


def _override_current_user(user: User):
    def dependency_override():
        return user

    return dependency_override


def test_get_profile_returns_current_user(client, db_session):
    user = User(
        name="Profile User",
        email="profile@example.com",
        phone_number="986666666666",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    client.app.dependency_overrides[dependencies.get_current_user] = _override_current_user(user)
    response = client.get("/users/profile")
    client.app.dependency_overrides.pop(dependencies.get_current_user, None)

    assert response.status_code == 200
    assert response.json()["email"] == "profile@example.com"


def test_update_profile_applies_valid_changes(client, db_session):
    user = User(
        name="Updater",
        email="update@example.com",
        phone_number="987777777777",
        role=UserRole.user,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    client.app.dependency_overrides[dependencies.get_current_user] = _override_current_user(user)

    response = client.patch(
        "/users/profile",
        json={"name": "Updated Name", "phone_number": "0912345678"},
    )
    client.app.dependency_overrides.pop(dependencies.get_current_user, None)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    # Phone numbers are normalized with country code prefix
    assert data["phone_number"].startswith("98")


def test_update_profile_rejects_duplicate_email(client, db_session):
    existing = User(
        name="Existing",
        email="existing@example.com",
        phone_number="988888888888",
        role=UserRole.user,
    )
    user = User(
        name="Target",
        email="target@example.com",
        phone_number="989999999999",
        role=UserRole.user,
    )
    db_session.add_all([existing, user])
    db_session.commit()
    db_session.refresh(user)

    client.app.dependency_overrides[dependencies.get_current_user] = _override_current_user(user)

    response = client.patch(
        "/users/profile",
        json={"email": "existing@example.com"},
    )
    client.app.dependency_overrides.pop(dependencies.get_current_user, None)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_update_profile_rejects_duplicate_phone(client, db_session):
    existing = User(
        name="Existing Phone",
        email="phone1@example.com",
        phone_number="981010101010",
        role=UserRole.user,
    )
    user = User(
        name="Target Phone",
        email="phone2@example.com",
        phone_number="981111111112",
        role=UserRole.user,
    )
    db_session.add_all([existing, user])
    db_session.commit()
    db_session.refresh(user)

    client.app.dependency_overrides[dependencies.get_current_user] = _override_current_user(user)

    response = client.patch(
        "/users/profile",
        json={"phone_number": "+1010101010"},
    )
    client.app.dependency_overrides.pop(dependencies.get_current_user, None)

    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number already registered"

