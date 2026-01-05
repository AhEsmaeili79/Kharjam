"""API dependencies"""
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db import get_db
from app.apps.auth.services import JWTService
from app.apps.auth.selectors import TokenSelector
from app.apps.auth.services import TokenBlacklistService
from app.apps.users.selectors import UserSelector
from app.apps.users.models import User
from app.core.errors import AuthError, UserError
from app.utils.google_drive import GoogleDriveService
from app.config.settings import google_drive_config

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials

    # Check Redis blacklist first (fast path)
    if TokenBlacklistService.is_blacklisted(token):
        raise HTTPException(status_code=401, detail=AuthError.TOKEN_BLACKLISTED)

    # Check database blacklist as fallback
    if TokenSelector.is_blacklisted(db, token):
        raise HTTPException(status_code=401, detail=AuthError.TOKEN_BLACKLISTED)

    # Decode token
    payload = JWTService.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail=AuthError.INVALID_TOKEN)

    # Get user
    user = UserSelector.get_by_id(db, payload["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail=UserError.NOT_FOUND)

    return user


def extract_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Extract token from Authorization header"""
    if not credentials:
        raise HTTPException(status_code=401, detail=AuthError.MISSING_AUTHORIZATION)
    return credentials.credentials


def get_drive_service() -> GoogleDriveService:
    """Get Google Drive service instance"""
    return GoogleDriveService(
        credentials_path=google_drive_config.credentials_path,
        folder_id=google_drive_config.folder_id
    )

