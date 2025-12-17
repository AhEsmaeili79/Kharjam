"""Auth schemas"""
from .auth import (
    RequestOTPRequest,
    RequestOTPResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
    TokenResponse,
    RefreshRequest,
    LogoutResponse,
)
from .errors import ErrorResponse

__all__ = [
    "RequestOTPRequest",
    "RequestOTPResponse",
    "VerifyOTPRequest",
    "VerifyOTPResponse",
    "TokenResponse",
    "RefreshRequest",
    "LogoutResponse",
    "ErrorResponse",
]

