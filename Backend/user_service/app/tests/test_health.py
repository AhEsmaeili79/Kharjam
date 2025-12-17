import pytest


def test_health_endpoint_returns_status(client, monkeypatch: pytest.MonkeyPatch):
    """Health endpoint should surface connectivity flags without hitting real services."""
    monkeypatch.setattr("app.core.health.check_db_connection", lambda: True)
    monkeypatch.setattr("app.core.health.check_redis_connection", lambda: False)
    monkeypatch.setattr("app.core.health.check_rabbitmq_connection", lambda: False)

    response = client.get("/health/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["services"]["database"]["connected"] is True
    assert payload["services"]["redis"]["connected"] is False
    assert payload["services"]["rabbitmq"]["connected"] is False

