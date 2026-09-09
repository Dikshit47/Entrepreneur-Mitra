"""Saved Scheme bookmark model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class SavedScheme(Base):
    __tablename__ = "saved_schemes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False, index=True)
    saved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint('user_id', 'scheme_id', name='uq_user_scheme_saved'),)

    user = relationship("User", back_populates="saved_schemes")
    scheme = relationship("Scheme")
