from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import AppError, ErrorCode
from app.models import User
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    email = login_data.email.lower()
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        if verify_password(login_data.password, user.password_hash):
            access_token = create_access_token(sub=user.id, role=user.role.value)
            return LoginResponse(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse.model_validate(user)
            )
        else:
            raise AppError(status_code=401, code=ErrorCode.INVALID_CREDENTIALS, message="Invalid credentials")
    else:
        verify_password(login_data.password, hash_password("dummy"))
        raise AppError(status_code=401, code=ErrorCode.INVALID_CREDENTIALS, message="Invalid credentials")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
