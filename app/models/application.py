"""Application model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False, index=True)
    selected_partner_id = Column(String(36), ForeignKey("partner_locations.id"), nullable=True)
    status = Column(String(40), default="DRAFT")  # DRAFT, DOCUMENTS_PREPARED, SUBMITTED_OFFICIALLY, SANCTIONED, REJECTED
    copilot_step = Column(Integer, default=1)  # 1: Eligibility, 2: Documents, 3: Prepare Application, 4: Official Channel, 5: Track
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="applications")
    scheme = relationship("Scheme")
    partner = relationship("PartnerLocation")
