import re
from fastapi import HTTPException

def normalize_phone_number(phone: str) -> str:
    """
    Normalize phone number by handling common formats:
    - Removes leading '+' if present
    - Handles Iran country code (+98 or 98) - keeps as 98XXXXXXXXXX
    - Handles local format starting with 0 - converts to 98XXXXXXXXXX
    """
    if not phone:
        return phone
    
    # Remove leading '+'
    phone = phone.lstrip('+')
    
    # Remove any whitespace
    phone = phone.strip()
    
    # Handle Iran country code: if starts with +98 or 98, keep as 98XXXXXXXXXX
    # If starts with 0 (local format), convert to 98XXXXXXXXXX
    if phone.startswith('0') and len(phone) == 11:
        # Convert local format (0XXXXXXXXXX) to international (98XXXXXXXXXX)
        phone = '98' + phone[1:]
    elif phone.startswith('98') and len(phone) >= 10:
        # Already in international format with country code
        pass
    elif not phone.startswith('98') and len(phone) == 10:
        # 10-digit number without country code, assume it's Iran and add 98
        phone = '98' + phone
    
    return phone

def validate_name(value):
    if not re.match(r"^[A-Za-z\s]{2,100}$", value):
        raise HTTPException(status_code=400, detail="Invalid name format")

def validate_phone_number(value):
    """Validate phone number - accepts formats like +98XXXXXXXXXX, 98XXXXXXXXXX, 0XXXXXXXXXX"""
    if not value:
        raise HTTPException(status_code=400, detail="Phone number cannot be empty")
    
    # Remove leading + for validation
    normalized = value.lstrip('+').strip()
    
    # Accept: 10-15 digits (can include country code)
    # Examples: 09123456789 (11 digits with 0), 989123456789 (12 digits with 98), +989123456789
    if not re.match(r"^\d{10,15}$", normalized):
        raise HTTPException(status_code=400, detail="Invalid phone number format. Expected 10-15 digits (e.g., +98XXXXXXXXXX, 98XXXXXXXXXX, 0XXXXXXXXXX)")

def validate_email(value):
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
        raise HTTPException(status_code=400, detail="Invalid email format")

def validate_card_number(value):
    if value and not re.match(r"^\d{16}$", value):
        raise HTTPException(status_code=400, detail="Invalid card number format")

def validate_card_holder_name(value):
    if value and not re.match(r"^[A-Za-z\s]{2,100}$", value):
        raise HTTPException(status_code=400, detail="Invalid card holder name format")

def validate_avatar_url(value):
    if value and not re.match(r"^https?://.+$", value):
        raise HTTPException(status_code=400, detail="Invalid avatar URL format")

def validate_role(value):
    if value not in ["user", "group_admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

FIELD_VALIDATORS = {
    "name": validate_name,
    "phone_number": validate_phone_number,
    "email": validate_email,
    "card_number": validate_card_number,
    "card_holder_name": validate_card_holder_name,
    "avatar_url": validate_avatar_url,
    "role": validate_role,
} 