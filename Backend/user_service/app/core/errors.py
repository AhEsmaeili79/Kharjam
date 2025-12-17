"""Standardized error messages for user-friendly API responses"""


# Authentication & Authorization errors
class AuthError:
    """Authentication and authorization error messages"""
    
    UNAUTHORIZED = "Authentication required"
    INVALID_TOKEN = "Invalid or expired token"
    TOKEN_BLACKLISTED = "Token has been revoked"
    INVALID_REFRESH_TOKEN = "Invalid or expired refresh token"
    MISSING_AUTHORIZATION = "Missing authorization header"


# User errors
class UserError:
    """User-related error messages"""
    
    NOT_FOUND = "User not found"
    OTP_NOT_REQUESTED = "Please request OTP first"
    INVALID_OTP = "Invalid or expired OTP code"
    PHONE_ALREADY_REGISTERED = "This phone number is already registered"
    EMAIL_ALREADY_REGISTERED = "This email is already registered"


# Validation errors
class ValidationError:
    """Validation error messages"""
    
    INVALID_NAME_FORMAT = "Name must be 2-100 characters and contain only letters and spaces"
    INVALID_PHONE_FORMAT = "Phone number must be 10-15 digits"
    PHONE_REQUIRED = "Phone number is required"
    INVALID_EMAIL_FORMAT = "Invalid email format"
    INVALID_CARD_NUMBER = "Card number must be 16 digits"
    INVALID_CARD_HOLDER_NAME = "Card holder name must be 2-100 characters and contain only letters and spaces"
    INVALID_AVATAR_URL = "Avatar URL must be a valid HTTP or HTTPS link"
    INVALID_ROLE = "Invalid role. Must be 'user' or 'group_admin'"

