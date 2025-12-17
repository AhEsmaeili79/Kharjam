"""Universal error response handlers"""
from typing import Dict
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


# Error code mapping based on HTTP status codes
STATUS_TO_ERROR_CODE: Dict[int, str] = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    429: "TOO_MANY_REQUESTS",
    500: "INTERNAL_ERROR",
    502: "BAD_GATEWAY",
    503: "SERVICE_UNAVAILABLE",
    504: "GATEWAY_TIMEOUT",
}

# Default user-friendly messages
STATUS_TO_MESSAGE: Dict[int, str] = {
    400: "Bad request",
    401: "Authentication required",
    403: "Access forbidden",
    404: "Resource not found",
    409: "Resource conflict",
    422: "Invalid request data",
    429: "Too many requests",
    500: "Something went wrong",
    502: "Bad gateway",
    503: "Service unavailable",
    504: "Gateway timeout",
}


def get_error_code(status_code: int) -> str:
    """Get error code for status code"""
    return STATUS_TO_ERROR_CODE.get(status_code, "INTERNAL_ERROR")


def get_default_message(status_code: int) -> str:
    """Get default message for status code"""
    return STATUS_TO_MESSAGE.get(status_code, "Something went wrong")


def extract_validation_fields(validation_errors: list) -> Dict[str, str]:
    """Extract field-level validation errors from FastAPI validation errors"""
    fields = {}
    for error in validation_errors:
        if isinstance(error, dict):
            # FastAPI validation errors have 'loc' (location tuple) and 'msg' (message)
            if "loc" in error and "msg" in error:
                loc = error["loc"]
                msg = error["msg"]
                
                # Extract field name from location tuple
                # FastAPI uses tuples like ('body', 'email') or ('query', 'limit')
                if loc and isinstance(loc, (list, tuple)):
                    # Get the last element as field name, skip 'body', 'query', 'path'
                    field_parts = [str(part) for part in loc if part not in ("body", "query", "path")]
                    if field_parts:
                        field = field_parts[-1]
                        # Use the last non-empty message if field already exists
                        if field in fields:
                            # Combine multiple errors for the same field
                            fields[field] = f"{fields[field]}; {msg}"
                        else:
                            fields[field] = msg
                elif loc:
                    # Fallback for non-tuple locations
                    field = str(loc[-1]) if isinstance(loc, (list, tuple)) else str(loc)
                    fields[field] = msg
    return fields


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException and convert to universal error format"""
    status_code = exc.status_code
    error_code = get_error_code(status_code)
    
    # Use exception detail as message, or default message
    message = str(exc.detail) if exc.detail else get_default_message(status_code)
    
    # Ensure message is safe for end users
    # Remove any technical details if needed
    if isinstance(exc.detail, dict):
        # If detail is a dict, extract message
        message = exc.detail.get("message", get_default_message(status_code))
    
    response_data = {
        "error": {
            "code": error_code,
            "message": message
        }
    }
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle RequestValidationError and convert to universal error format with fields"""
    errors = exc.errors()
    fields = extract_validation_fields(errors)
    
    # Build a general message from validation errors
    if fields:
        # Use first field error as primary message, or generic message
        first_field = list(fields.keys())[0]
        first_error = fields[first_field]
        message = f"Validation failed: {first_error}"
    else:
        message = "Invalid request data"
    
    response_data = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "fields": fields
        }
    }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_data
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions and convert to universal error format"""
    # Log the exception for debugging
    logger.exception(f"Unhandled exception: {exc}")
    
    response_data = {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "Something went wrong"
        }
    }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_data
    )

