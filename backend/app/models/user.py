import uuid
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func
import enum


class Base(DeclarativeBase):
    pass


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.MEMBER)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_users_email_lower", "email", postgresql_ops={"email": "LOWER"}, unique=True),
    )

    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="user")
