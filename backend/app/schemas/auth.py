from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal
from app.models import UserRole


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1, max_length=255)

    @field_validator('email')
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        return v.lower()

    @field_validator('password')
    @classmethod
    def password_trim(cls, v: str) -> str:
        return v.strip()


class UserResponse(BaseModel):
    id: str
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    user: UserResponse
