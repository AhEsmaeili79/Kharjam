"""Validation utilities"""
import re
from fastapi import HTTPException
from app.core.errors import ValidationError


def normalize_phone_number(phone: str) -> str:
    """Normalize phone number to standard format"""
    if not phone:
        return phone

    phone = phone.lstrip('+').strip()

    if phone.startswith('0') and len(phone) == 11:
        phone = '98' + phone[1:]
    elif phone.startswith('98') and len(phone) >= 10:
        pass
    elif not phone.startswith('98') and len(phone) == 10:
        phone = '98' + phone

    return phone


def validate_name(value: str):
    """Validate name format"""
    if not re.match(r"^[A-Za-z\s]{2,100}$", value):
        raise HTTPException(status_code=400, detail=ValidationError.INVALID_NAME_FORMAT)


def validate_phone_number(value: str):
    """Validate phone number format"""
    if not value:
        raise HTTPException(status_code=400, detail=ValidationError.PHONE_REQUIRED)

    normalized = value.lstrip('+').strip()
    if not re.match(r"^\d{10,15}$", normalized):
        raise HTTPException(status_code=400, detail=ValidationError.INVALID_PHONE_FORMAT)


def validate_email(value: str):
    """Validate email format"""
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
        raise HTTPException(status_code=400, detail=ValidationError.INVALID_EMAIL_FORMAT)


def validate_card_number(value: str):
    """Validate card number format"""
    if value and not re.match(r"^\d{16}$", value):
        raise HTTPException(status_code=400, detail=ValidationError.INVALID_CARD_NUMBER)


def validate_card_holder_name(value: str):
    """Validate card holder name format"""
    if value and not re.match(r"^[A-Za-z\s]{2,100}$", value):
        raise HTTPException(status_code=400, detail=ValidationError.INVALID_CARD_HOLDER_NAME)


def validate_avatar_url(value: str):
    """Validate avatar URL format"""
    if value and not re.match(r"^https?://.+$", value):
        raise HTTPException(status_code=400, detail=ValidationError.INVALID_AVATAR_URL)


def validate_role(value: str):
    """Validate role value"""
    if value not in ["user", "group_admin"]:
        raise HTTPException(status_code=400, detail=ValidationError.INVALID_ROLE)


FIELD_VALIDATORS = {
    "name": validate_name,
    "phone_number": validate_phone_number,
    "email": validate_email,
    "card_number": validate_card_number,
    "card_holder_name": validate_card_holder_name,
    "avatar_url": validate_avatar_url,
    "role": validate_role,
}

