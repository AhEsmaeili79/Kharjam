"""Common error response schemas for API documentation"""
from typing import Optional, Dict
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Error detail schema matching universal error format"""
    code: str
    message: str
    fields: Optional[Dict[str, str]] = None


class ErrorResponse(BaseModel):
    """Universal error response schema"""
    error: ErrorDetail



