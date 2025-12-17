"""JWT token service"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.config import jwt_config


class JWTService:
    """JWT token service"""

    @staticmethod
    def create_access_token(data: Dict) -> str:
        """Create access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=jwt_config.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, jwt_config.secret_key, algorithm=jwt_config.algorithm)

    @staticmethod
    def create_refresh_token(data: Dict) -> str:
        """Create refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=jwt_config.refresh_token_expire_days)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, jwt_config.refresh_secret_key, algorithm=jwt_config.algorithm)

    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict]:
        """Decode access token"""
        try:
            return jwt.decode(token, jwt_config.secret_key, algorithms=[jwt_config.algorithm])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def decode_refresh_token(token: str) -> Optional[Dict]:
        """Decode refresh token"""
        try:
            return jwt.decode(token, jwt_config.refresh_secret_key, algorithms=[jwt_config.algorithm])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

