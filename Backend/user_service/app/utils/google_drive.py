"""Google Drive utility for file storage"""
import os
import io
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class GoogleDriveService:
    """Google Drive service for file operations"""
    
    def __init__(self, credentials_path: str, folder_id: str):
        """
        Initialize Google Drive service
        
        Args:
            credentials_path: Path to client_secret.json
            folder_id: Google Drive folder ID where files will be stored
        """
        self.credentials_path = credentials_path
        self.folder_id = folder_id
        self.service = None
        self._creds = None
        # Don't authenticate at init - do it lazily when needed
    
    def _authenticate(self):
        """Authenticate and build Google Drive service"""
        if self.service is not None:
            return  # Already authenticated
        
        creds = None
        token_path = 'token.json'
        
        # Load existing token if available
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception:
                # Token file is invalid, will need to re-authenticate
                creds = None
        
        # If there are no valid credentials, request authorization
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    # Refresh failed, need to re-authenticate
                    creds = None
            
            if not creds or not creds.valid:
                # Check if credentials file exists
                if not os.path.exists(self.credentials_path):
                    raise HTTPException(
                        status_code=500,
                        detail=f"Google Drive credentials file not found: {self.credentials_path}. Please ensure client_secret.json exists."
                    )
                
                # Try to authenticate - in Docker, this will fail if no token.json exists
                # User must pre-authenticate and provide token.json
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    # Try local server first (for local dev)
                    try:
                        creds = flow.run_local_server(port=0, open_browser=False)
                    except Exception:
                        # In Docker, we can't authenticate interactively
                        # User must provide token.json
                        raise HTTPException(
                            status_code=500,
                            detail=(
                                "Google Drive authentication required. token.json not found.\n"
                                "To generate token.json:\n"
                                "1. Run the service locally (outside Docker) once\n"
                                "2. Complete OAuth flow in browser\n"
                                "3. Copy token.json to Docker container at /user_service/token.json"
                            )
                        )
                    
                    # Save credentials for next run
                    if creds:
                        with open(token_path, 'w') as token:
                            token.write(creds.to_json())
                except HTTPException:
                    raise
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Google Drive authentication failed: {str(e)}. Please ensure token.json exists."
                    )
        
        self._creds = creds
        self.service = build('drive', 'v3', credentials=creds)
    
    def upload_file(self, file: UploadFile, user_id: str) -> str:
        """
        Upload file to Google Drive
        
        Args:
            file: FastAPI UploadFile object
            user_id: User ID for naming the file
            
        Returns:
            URL with filename format: gdrive://{file_id}/{filename}
            This format will be converted to a proper endpoint URL by the route handler
            
        Raises:
            HTTPException: If upload fails
        """
        # Authenticate if not already done
        self._authenticate()
        
        try:
            # Read file content
            file_content = file.file.read()
            file.file.seek(0)  # Reset file pointer
            
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1] if file.filename else '.jpg'
            filename = f"profile_{user_id}_{uuid.uuid4().hex[:8]}{file_extension}"
            
            # Create file metadata
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            # Create media upload
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=file.content_type or 'image/jpeg',
                resumable=True
            )
            
            # Upload file
            uploaded_file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            # Make file publicly viewable
            self.service.permissions().create(
                fileId=uploaded_file['id'],
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            
            # Return custom format: gdrive://{file_id}/{filename}
            # This will be converted to /users/avatar/{filename} endpoint
            file_id = uploaded_file['id']
            file_url = f"gdrive://{file_id}/{filename}"
            
            return file_url
            
        except HttpError as error:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to Google Drive: {str(error)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error during file upload: {str(e)}"
            )
    
    def delete_file(self, file_url: str) -> bool:
        """
        Delete file from Google Drive using file URL
        
        Args:
            file_url: Google Drive file URL
            
        Returns:
            True if deleted successfully, False otherwise
        """
        # Authenticate if not already done
        self._authenticate()
        
        try:
            # Extract file ID from URL
            file_id = self._extract_file_id(file_url)
            if not file_id:
                return False
            
            # Delete file
            self.service.files().delete(fileId=file_id).execute()
            return True
            
        except HttpError as error:
            if error.resp.status == 404:
                # File not found, consider it deleted
                return True
            return False
        except Exception:
            return False
    
    def _extract_file_id(self, url: str) -> Optional[str]:
        """
        Extract file ID from Google Drive URL
        
        Args:
            url: Google Drive URL (various formats)
                - gdrive://{file_id}/{filename}
                - https://drive.google.com/uc?export=view&id=FILE_ID
                - https://drive.google.com/file/d/FILE_ID/view
            
        Returns:
            File ID or None if not found
        """
        # Handle custom gdrive:// format
        if url.startswith('gdrive://'):
            # Format: gdrive://{file_id}/{filename}
            parts = url.replace('gdrive://', '').split('/')
            if parts:
                return parts[0]
        
        # Handle different URL formats
        if 'id=' in url:
            # Format: https://drive.google.com/uc?export=view&id=FILE_ID
            return url.split('id=')[1].split('&')[0]
        elif '/file/d/' in url:
            # Format: https://drive.google.com/file/d/FILE_ID/view
            parts = url.split('/file/d/')
            if len(parts) > 1:
                return parts[1].split('/')[0]
        elif '/folders/' in url:
            # This is a folder URL, not a file
            return None
        
        return None
    
    def get_file_view_url(self, file_id: str) -> str:
        """
        Get direct view URL for a Google Drive file (public access)
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            Direct view URL
        """
        return f"https://drive.google.com/uc?export=view&id={file_id}"


def convert_gdrive_url_to_endpoint_url(gdrive_url: Optional[str], base_url: str) -> Optional[str]:
    """
    Convert gdrive:// URL format to proper endpoint URL
    
    Args:
        gdrive_url: URL in format gdrive://{file_id}/{filename}
        base_url: Base URL for the API (from request.base_url)
        
    Returns:
        Proper endpoint URL or None if invalid
    """
    if not gdrive_url or not gdrive_url.startswith('gdrive://'):
        return gdrive_url
    
    # Extract filename from gdrive://{file_id}/{filename}
    parts = gdrive_url.replace('gdrive://', '').split('/', 1)
    if len(parts) == 2:
        filename = parts[1]
        base_url = base_url.rstrip('/')
        return f"{base_url}/users/avatar/{filename}"
    
    return gdrive_url
