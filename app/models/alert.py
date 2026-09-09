"""Alert notifications model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=True)
    alert_type = Column(String(50), default="SCHEME_UPDATE")  # SCHEME_UPDATE, DEADLINE, ELIGIBILITY_CHANGE
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    payload_json = Column(Text, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="alerts")
    scheme = relationship("Scheme")
