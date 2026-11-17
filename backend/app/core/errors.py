from typing import Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


class ErrorCode:
    UNAUTHENTICATED = "UNAUTHENTICATED"
    FORBIDDEN = "FORBIDDEN"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    SNACK_NOT_FOUND = "SNACK_NOT_FOUND"
    SNACK_NAME_TAKEN = "SNACK_NAME_TAKEN"
    INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"
    ALREADY_VOTED = "ALREADY_VOTED"
    VOTE_NOT_FOUND = "VOTE_NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    # Convert any bytes in errors to strings
    for error in errors:
        for key, value in error.items():
            if isinstance(value, bytes):
                error[key] = value.decode('utf-8', errors='replace')
            elif isinstance(value, list):
                error[key] = [
                    v.decode('utf-8', errors='replace') if isinstance(v, bytes) else v
                    for v in value
                ]
    field_names = [err["loc"][-1] for err in errors if err["loc"]]
    message = f"Validation failed for: {', '.join(field_names)}"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": ErrorCode.VALIDATION_ERROR,
                "message": message,
                "details": errors
            }
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        code = ErrorCode.NOT_FOUND
        message = "Resource not found"
    elif exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        code = ErrorCode.METHOD_NOT_ALLOWED
        message = "Method not allowed"
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        code = ErrorCode.UNAUTHENTICATED
        message = exc.detail or "Not authenticated"
    else:
        code = ErrorCode.INTERNAL_ERROR
        message = exc.detail or "An error occurred"
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": code, "message": message}}
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    logger.error(f"Database integrity error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": {"code": ErrorCode.INTERNAL_ERROR, "message": "Data conflict"}}
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": ErrorCode.INTERNAL_ERROR, "message": "Internal server error"}}
    )

