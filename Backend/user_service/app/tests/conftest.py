import os
from typing import Callable, Dict, List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Force test database to lightweight SQLite, overriding any env-provided DSN
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
# Set required secrets before importing application modules
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("REFRESH_SECRET_KEY", "test-refresh-secret")

from app.db import Base, get_db  # noqa: E402  pylint: disable=wrong-import-position
from app.main import app  # noqa: E402  pylint: disable=wrong-import-position


TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


class FakeCache:
    """In-memory cache used to stub Redis during tests."""

    def __init__(self):
        self.store: Dict[str, object] = {}

    def get(self, key: str):
        return self.store.get(key)

    def set(self, key: str, value, expire: int | None = None) -> bool:
        self.store[key] = value
        return True

    def delete(self, key: str) -> bool:
        return self.store.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        return key in self.store


class FakeProducer:
    """Stub for RabbitMQ producer interactions."""

    def __init__(self):
        self.otp_messages: List[Dict[str, object]] = []
        self.messages: List[Dict[str, object]] = []

    def publish_otp_message(self, identifier: str, otp_code: str, routing_key: str) -> bool:
        self.otp_messages.append(
            {"identifier": identifier, "otp_code": otp_code, "routing_key": routing_key}
        )
        return True

    def publish_message(self, exchange: str, routing_key: str, message: Dict[str, object], correlation_id: str | None = None) -> bool:
        self.messages.append(
            {
                "exchange": exchange,
                "routing_key": routing_key,
                "message": message,
                "correlation_id": correlation_id,
            }
        )
        return True


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """Create and drop all tables for tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if TEST_DATABASE_URL.startswith("sqlite:///./") and os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture()
def db_session():
    """Provide a database session wrapped in a transaction per test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def fake_cache(monkeypatch: pytest.MonkeyPatch) -> FakeCache:
    """Patch Redis dependencies with an in-memory cache."""
    cache = FakeCache()
    monkeypatch.setattr("app.core.redis.cache.get_cache", lambda: cache)
    monkeypatch.setattr("app.core.redis.get_cache", lambda: cache)
    monkeypatch.setattr("app.apps.auth.services.otp_service.get_cache", lambda: cache)
    monkeypatch.setattr(
        "app.apps.auth.services.token_blacklist_service.get_cache", lambda: cache
    )
    return cache


@pytest.fixture()
def fake_producer(monkeypatch: pytest.MonkeyPatch) -> FakeProducer:
    """Patch RabbitMQ producer dependencies with an in-memory stub."""
    producer = FakeProducer()
    monkeypatch.setattr("app.core.rabbitmq.get_rabbitmq_producer", lambda: producer)
    monkeypatch.setattr("app.apps.auth.services.otp_service.get_rabbitmq_producer", lambda: producer)
    monkeypatch.setattr("app.tasks.user_lookup_consumer.get_rabbitmq_producer", lambda: producer)
    return producer


@pytest.fixture()
def client(
    db_session,
    fake_cache: FakeCache,
    fake_producer: FakeProducer,
    monkeypatch: pytest.MonkeyPatch,
):
    """FastAPI TestClient with DB override and external services stubbed."""
    # Prevent startup hooks from touching external services
    monkeypatch.setattr("app.main.init_rabbitmq", lambda: None)
    monkeypatch.setattr("app.main.init_redis", lambda: None)
    monkeypatch.setattr("app.main.start_consumer", lambda: None)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)

