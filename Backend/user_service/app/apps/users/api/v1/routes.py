"""User API routes"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, Response
from typing import Optional
from sqlalchemy.orm import Session
import httpx
from app.db import get_db
from app.apps.users.models import User
from app.apps.users.schemas import UserOut, UserUpdate, ErrorResponse
from app.apps.users.services import UserService
from app.core.dependencies import get_current_user, get_drive_service
from app.utils.google_drive import convert_gdrive_url_to_endpoint_url, GoogleDriveService
from app.utils.validators import validate_image_file

router = APIRouter(prefix="/users", tags=["Users"])


def _convert_user_avatar_url(user: User, request: Request) -> UserOut:
    """Convert user avatar URL from gdrive:// format to endpoint URL"""
    user_out = UserOut.model_validate(user)
    if user_out.avatar_url and user_out.avatar_url.startswith('gdrive://'):
        user_out.avatar_url = convert_gdrive_url_to_endpoint_url(
            user_out.avatar_url, str(request.base_url)
        )
    return user_out


def _handle_avatar_deletion(user: User, drive_service: GoogleDriveService):
    """Helper to delete avatar if exists"""
    if user.avatar_url:
        drive_service.delete_file(user.avatar_url)
        user.avatar_url = None


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
    request: Request,
    current_user: User = Depends(get_current_user)
) -> UserOut:
    """Get current user profile"""
    return _convert_user_avatar_url(current_user, request)


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
    request: Request,
    name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    card_number: Optional[str] = Form(None),
    card_holder_name: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    delete_profile_image: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    drive_service: GoogleDriveService = Depends(get_drive_service)
) -> UserOut:
    """Update user profile"""
    # Handle profile image upload
    if profile_image and profile_image.filename and profile_image.filename.strip():
        validate_image_file(profile_image)
        _handle_avatar_deletion(current_user, drive_service)
        current_user.avatar_url = drive_service.upload_file(profile_image, current_user.id)
    
    # Handle profile image deletion
    elif delete_profile_image and delete_profile_image.lower() in ('true', '1', 'yes'):
        _handle_avatar_deletion(current_user, drive_service)
    
    # Update other fields if provided
    update_fields = {
        'name': name,
        'phone_number': phone_number,
        'email': email,
        'card_number': card_number,
        'card_holder_name': card_holder_name
    }
    update_data = {k: v for k, v in update_fields.items() if v is not None}
    
    if update_data:
        UserService.validate_and_update_user(current_user, UserUpdate(**update_data), db)
    
    db.commit()
    db.refresh(current_user)
    return _convert_user_avatar_url(current_user, request)


@router.get(
    "/avatar/{filename:path}",
    operation_id="getAvatarApi",
    include_in_schema=False,
    responses={
        404: {"model": ErrorResponse, "description": "Avatar not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_avatar(
    filename: str,
    db: Session = Depends(get_db),
    drive_service: GoogleDriveService = Depends(get_drive_service)
) -> Response:
    """Get avatar image from Google Drive"""
    # Find user with avatar_url containing this filename
    user = db.query(User).filter(User.avatar_url.like(f'%{filename}')).first()
    
    if not user or not user.avatar_url:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    file_id = drive_service._extract_file_id(user.avatar_url)
    if not file_id:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    # Fetch image from Google Drive
    view_url = drive_service.get_file_view_url(file_id)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(view_url, follow_redirects=True, timeout=30.0)
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Avatar not found")
            
            # Determine content type from filename extension
            content_type = "image/png" if filename.lower().endswith('.png') else "image/jpeg"
            
            return Response(
                content=response.content,
                media_type=content_type,
                headers={
                    "Content-Disposition": f'inline; filename="{filename}"',
                    "Cache-Control": "public, max-age=31536000",
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch avatar: {str(e)}")

