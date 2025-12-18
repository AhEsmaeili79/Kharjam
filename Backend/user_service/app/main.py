"""Main application entry point"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

# Import models to ensure they're registered with SQLAlchemy Base metadata
from app.apps.users.models import User
from app.apps.auth.models import OtpCode, BlacklistedToken
from app.apps.users.api import router as users_router
from app.apps.auth.api import router as auth_router
from app.core.health import router as health_router
from app.core.rabbitmq import (
    init_rabbitmq,
    start_user_lookup_consumer,
    stop_user_lookup_consumer,
    start_user_info_consumer,
    stop_user_info_consumer,
)
from app.core.redis.init import init_redis
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)
from app.config import app_config


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """Application lifespan context to manage startup/shutdown hooks."""
    # Startup
    init_rabbitmq()
    init_redis()
    start_user_lookup_consumer()
    start_user_info_consumer()
    
    yield
    
    # Shutdown
    stop_user_lookup_consumer()
    stop_user_info_consumer()


app = FastAPI(
    title="User Service",
    description="User management service with RabbitMQ and Redis integration",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins.split(",") if app_config.cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Register exception handlers for universal error response format
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)

