from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.db import get_db
from app.core.config import settings
from app.core.errors import (
    AppError,
    app_error_handler,
    validation_error_handler,
    http_exception_handler,
    integrity_error_handler,
    general_exception_handler
)
from app.api.routes.auth import router as auth_router
from app.api.routes.snacks import router as snacks_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError

app = FastAPI(
    title="Snack Overflow API",
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
    openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
)

# CORS configuration
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Register error handlers
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)

# Include routers
app.include_router(auth_router)
app.include_router(snacks_router)


@app.get("/health")
def health_check():
    """Health check endpoint that verifies database connectivity."""
    db = next(get_db())
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    finally:
        db.close()
