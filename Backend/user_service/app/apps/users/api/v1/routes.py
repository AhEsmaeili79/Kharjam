"""User API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.apps.users.models import User
from app.apps.users.schemas import UserOut, UserUpdate, ErrorResponse
from app.apps.users.services import UserService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/profile",
    response_model=UserOut,
    operation_id="getProfileApi",
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid or missing token"},
        404: {"model": ErrorResponse, "description": "User not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserOut:
    """Get current user profile"""
    return current_user


@router.patch(
    "/profile",
    response_model=UserOut,
    operation_id="updateProfileApi",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request - Validation error or duplicate phone/email"},
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid or missing token"},
        404: {"model": ErrorResponse, "description": "User not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def update_user_profile(
    update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserOut:
    """Update user profile"""
    user = UserService.validate_and_update_user(current_user, update, db)
    db.commit()
    db.refresh(user)
    return user

