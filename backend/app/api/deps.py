from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import decode_access_token
from app.core.errors import AppError, ErrorCode
from app.models import User, UserRole

security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    
    if user_id is None:
        raise AppError(status_code=401, code=ErrorCode.UNAUTHENTICATED, message="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise AppError(status_code=401, code=ErrorCode.UNAUTHENTICATED, message="User not found")
    
    return user


def require_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != UserRole.ADMIN:
        raise AppError(status_code=403, code=ErrorCode.FORBIDDEN, message="Admin access required")
    return current_user

