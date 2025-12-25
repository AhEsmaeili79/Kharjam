"""User API routes"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from sqlalchemy.orm import Session
from app.db import get_db
from app.apps.users.models import User
from app.apps.users.schemas import UserOut, UserUpdate, ErrorResponse
from app.apps.users.services import UserService
from app.core.dependencies import get_current_user
from app.utils.google_drive import GoogleDriveService
from app.utils.validators import validate_image_file
from app.config.settings import google_drive_config

router = APIRouter(prefix="/users", tags=["Users"])


def get_drive_service() -> GoogleDriveService:
    """Get Google Drive service instance"""
    return GoogleDriveService(
        credentials_path=google_drive_config.credentials_path,
        folder_id=google_drive_config.folder_id
    )


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
async def update_user_profile(
    name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    card_number: Optional[str] = Form(None),
    card_holder_name: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    delete_profile_image: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserOut:
    """
    Update user profile
    
    Supports multipart/form-data for file uploads:
    - Upload new profile image: send profile_image file (jpg, jpeg, png, max 5MB)
    - Delete profile image: set delete_profile_image=true or "true"
    - Update other fields: send as form fields
    
    Note: For file uploads, use multipart/form-data. For JSON-only updates,
    you can still use form-data without the file field.
    """
    drive_service = get_drive_service()
    
    # Handle profile image upload
    if profile_image is not None:
        # Check if file has a filename (empty file uploads are ignored)
        if not profile_image.filename or not profile_image.filename.strip():
            # Empty file upload, skip it
            pass
        else:
            # Validate image file
            validate_image_file(profile_image)
            
            # Delete old image if exists
            if current_user.avatar_url:
                drive_service.delete_file(current_user.avatar_url)
            
            # Upload new image
            avatar_url = drive_service.upload_file(profile_image, current_user.id)
            current_user.avatar_url = avatar_url
    
    # Handle profile image deletion
    elif delete_profile_image and delete_profile_image.lower() in ('true', '1', 'yes'):
        if current_user.avatar_url:
            drive_service.delete_file(current_user.avatar_url)
            current_user.avatar_url = None
    
    # Prepare update data
    update_data = {}
    if name is not None:
        update_data['name'] = name
    if phone_number is not None:
        update_data['phone_number'] = phone_number
    if email is not None:
        update_data['email'] = email
    if card_number is not None:
        update_data['card_number'] = card_number
    if card_holder_name is not None:
        update_data['card_holder_name'] = card_holder_name
    
    # Update other fields if provided
    if update_data:
        update = UserUpdate(**update_data)
        user = UserService.validate_and_update_user(current_user, update, db)
    else:
        user = current_user
    
    db.commit()
    db.refresh(user)
    return user

