import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.user import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    snack_id = Column(String, ForeignKey("snacks.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "snack_id", name="uq_user_snack"),
        Index("ix_votes_snack_id", "snack_id"),
    )

    user = relationship("User", back_populates="votes")
    snack = relationship("Snack", back_populates="votes")
