"""Auth schemas"""
from pydantic import BaseModel, field_validator
from typing import Optional


class RequestOTPRequest(BaseModel):
    """Request OTP schema"""
    identifier: str

    @field_validator('identifier')
    @classmethod
    def validate_identifier(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Identifier cannot be empty')
        return v.strip()


class RequestOTPResponse(BaseModel):
    """Request OTP response schema"""
    message: str
    identifier_type: str
    otp_code: Optional[str] = None


class VerifyOTPRequest(BaseModel):
    """Verify OTP schema"""
    identifier: str
    otp_code: str

    @field_validator('identifier')
    @classmethod
    def validate_identifier(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Identifier cannot be empty')
        return v.strip()

    @field_validator('otp_code')
    @classmethod
    def validate_otp_code(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('OTP code cannot be empty')
        if len(v.strip()) != 5:
            raise ValueError('OTP code must be 5 digits')
        if not v.strip().isdigit():
            raise ValueError('OTP code must contain only digits')
        return v.strip()


class UserData(BaseModel):
    """User data schema"""
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class VerifyOTPResponse(BaseModel):
    """Verify OTP response schema"""
    access_token: str
    refresh_token: str
    user_data: UserData
    is_new_user: bool


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class LogoutResponse(BaseModel):
    """Logout response schema"""
    msg: str

