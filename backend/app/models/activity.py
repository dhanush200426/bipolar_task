import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import Base
import enum


class ActivityAction(str, enum.Enum):
    RESTOCKED = "restocked"
    CONSUMED = "consumed"


class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    snack_id = Column(String, ForeignKey("snacks.id", ondelete="SET NULL"), nullable=True)
    snack_name = Column(String, nullable=False)
    action = Column(SQLEnum(ActivityAction), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
        Index("ix_activities_created_at", "created_at"),
        Index("ix_activities_snack_id", "snack_id"),
    )

    user = relationship("User", back_populates="activities")
    snack = relationship("Snack", back_populates="activities")
