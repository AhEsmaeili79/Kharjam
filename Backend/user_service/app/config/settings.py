"""
Application configuration settings
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


# =========================
# Database Configuration
# =========================

class DatabaseConfig(BaseSettings):
    db: str
    user: str
    password: str
    host: str = "postgres"
    port: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="POSTGRES_",
        case_sensitive=False,
        extra="ignore",
    )


# =========================
# Redis Configuration
# =========================

class RedisConfig(BaseSettings):
    host: str = "redis"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0
    max_connections: int = 20
    socket_timeout: int = 5
    socket_connect_timeout: int = 5

    @property
    def redis_url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        case_sensitive=False,
        extra="ignore",
    )


# =========================
# RabbitMQ Configuration
# =========================

class RabbitMQConfig(BaseSettings):
    host: str
    port: int = 5672
    username: str
    password: str
    virtual_host: str = "/"
    connection_attempts: int = 3
    retry_delay: float = 2.0
    heartbeat: int = 600
    message_ttl: int = 300000

    # Exchanges
    otp_exchange: str = "user.otp.exchange"
    user_lookup_exchange: str = "user.lookup.exchange"
    exchange_type: str = "topic"

    # User info RPC (direct exchange)
    user_info_exchange: str = "user_info_exchange"
    user_info_exchange_type: str = "direct"

    # Queues
    email_queue: str = "user.otp.email.queue"
    sms_queue: str = "user.otp.sms.queue"
    user_lookup_request_queue: str = "user.lookup.request.queue"
    user_lookup_response_queue: str = "user.lookup.response.queue"

    # User info RPC queues
    user_info_request_queue: str = "user_info_request_queue"

    # Routing Keys
    email_routing_key: str = "otp.email.send"
    sms_routing_key: str = "otp.sms.send"
    user_lookup_request_key: str = "user.lookup.request"
    user_lookup_response_key: str = "user.lookup.response"
    user_info_request_routing_key: str = "user_info_request"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RABBITMQ_",
        case_sensitive=False,
        extra="ignore",
    )


# =========================
# JWT Configuration
# =========================

class JWTConfig(BaseSettings):
    secret_key: str
    refresh_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


# =========================
# Application Configuration
# =========================

class AppConfig(BaseSettings):
    pythonpath: Optional[str] = None
    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


# =========================
# Google Drive Configuration
# =========================

class GoogleDriveConfig(BaseSettings):
    folder_id: str
    credentials_path: str = "client_secret.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="GOOGLE_DRIVE_",
        case_sensitive=False,
        extra="ignore",
    )


# =========================
# Global Instances
# =========================

database_config = DatabaseConfig()
redis_config = RedisConfig()
rabbitmq_config = RabbitMQConfig()
jwt_config = JWTConfig()
app_config = AppConfig()
google_drive_config = GoogleDriveConfig()
