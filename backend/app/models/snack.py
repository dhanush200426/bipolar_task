import uuid
from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import Base
import enum


class SnackCategory(str, enum.Enum):
    SWEET = "sweet"
    SAVOURY = "savoury"
    DRINK = "drink"
    HEALTHYISH = "healthy-ish"


class Snack(Base):
    __tablename__ = "snacks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    category = Column(SQLEnum(SnackCategory), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    low_stock_threshold = Column(Integer, nullable=False, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_non_negative"),
        CheckConstraint("low_stock_threshold >= 0", name="check_low_stock_threshold_non_negative"),
        Index("ix_snacks_name_lower", "name", postgresql_ops={"name": "LOWER"}, unique=True),
        Index("ix_snacks_category", "category"),
    )

    votes = relationship("Vote", back_populates="snack", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="snack")
