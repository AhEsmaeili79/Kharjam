"""Auth models"""
from .otp_code import OtpCode
from .blacklisted_token import BlacklistedToken

__all__ = ["OtpCode", "BlacklistedToken"]

