"""User API routes"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, Response
from typing import Optional
from sqlalchemy.orm import Session
import httpx
from app.db import get_db, SessionLocal
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


def convert_gdrive_url_to_endpoint_url(gdrive_url: Optional[str], request: Request) -> Optional[str]:
    """
    Convert gdrive:// URL format to proper endpoint URL
    
    Args:
        gdrive_url: URL in format gdrive://{file_id}/{filename}
        request: FastAPI Request object to get base URL
        
    Returns:
        Proper endpoint URL or None if invalid
    """
    if not gdrive_url:
        return None
    
    if gdrive_url.startswith('gdrive://'):
        # Extract filename from gdrive://{file_id}/{filename}
        parts = gdrive_url.replace('gdrive://', '').split('/', 1)
        if len(parts) == 2:
            filename = parts[1]
            # Return endpoint URL with filename
            base_url = str(request.base_url).rstrip('/')
            return f"{base_url}/users/avatar/{filename}"
    
    # Return as-is if already a proper URL
    return gdrive_url


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
    # Convert avatar_url if it's in gdrive:// format
    if current_user.avatar_url and current_user.avatar_url.startswith('gdrive://'):
        # Create a temporary user object with converted URL
        user_dict = {
            **current_user.__dict__,
            'avatar_url': convert_gdrive_url_to_endpoint_url(current_user.avatar_url, request)
        }
        # Remove SQLAlchemy internal attributes
        user_dict.pop('_sa_instance_state', None)
        return UserOut(**user_dict)
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
    request: Request,
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
    
    # Convert avatar_url if it's in gdrive:// format
    if user.avatar_url and user.avatar_url.startswith('gdrive://'):
        # Create a temporary user object with converted URL
        user_dict = {
            **user.__dict__,
            'avatar_url': convert_gdrive_url_to_endpoint_url(user.avatar_url, request)
        }
        # Remove SQLAlchemy internal attributes
        user_dict.pop('_sa_instance_state', None)
        return UserOut(**user_dict)
    
    return user


@router.get(
    "/avatar/{filename:path}",
    operation_id="getAvatarApi",
    responses={
        404: {"model": ErrorResponse, "description": "Avatar not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_avatar(
    filename: str,
    request: Request
) -> Response:
    """
    Proxy endpoint to serve avatar images from Google Drive with proper filename
    
    The filename should be in format: profile_{user_id}_{uuid}.{extension}
    This endpoint fetches the image from Google Drive and serves it with proper headers.
    """
    drive_service = get_drive_service()
    
    try:
        # Extract file_id from filename by looking up in database
        # Since we store gdrive://{file_id}/{filename}, we need to find the user with this filename
        db = SessionLocal()
        try:
            # Find user with avatar_url containing this filename
            user = db.query(User).filter(
                User.avatar_url.like(f'%{filename}')
            ).first()
            
            if not user or not user.avatar_url:
                raise HTTPException(status_code=404, detail="Avatar not found")
            
            # Extract file_id from gdrive:// URL
            if user.avatar_url.startswith('gdrive://'):
                file_id = drive_service._extract_file_id(user.avatar_url)
            else:
                # Legacy format - extract from old URL
                file_id = drive_service._extract_file_id(user.avatar_url)
            
            if not file_id:
                raise HTTPException(status_code=404, detail="Avatar not found")
            
            # Get view URL from Google Drive (public access)
            view_url = drive_service.get_file_view_url(file_id)
            
            # Fetch image from Google Drive
            async with httpx.AsyncClient() as client:
                response = await client.get(view_url, follow_redirects=True, timeout=30.0)
                if response.status_code != 200:
                    raise HTTPException(status_code=404, detail="Avatar not found")
                
                # Determine content type from filename extension
                content_type = "image/jpeg"
                if filename.lower().endswith('.png'):
                    content_type = "image/png"
                elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    content_type = "image/jpeg"
                
                # Return image with proper headers and filename
                return Response(
                    content=response.content,
                    media_type=content_type,
                    headers={
                        "Content-Disposition": f'inline; filename="{filename}"',
                        "Cache-Control": "public, max-age=31536000",  # Cache for 1 year
                    }
                )
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch avatar: {str(e)}"
        )

