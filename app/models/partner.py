"""Partner Location and Geo-spatial routing models."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime
from app.database import Base


class PartnerLocation(Base):
    __tablename__ = "partner_locations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    partner_name = Column(String(150), nullable=False)
    partner_type = Column(String(50), default="SCA")  # SCA, RRB, NATIONALISED_BANK, NBFC
    scheme_categories = Column(String(200), default="CREDIT_LOAN,MICRO_FINANCE")
    address = Column(String(255), nullable=False)
    district = Column(String(60), nullable=False, index=True)
    state = Column(String(60), nullable=False, index=True)
    pincode = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    fund_utilisation_status = Column(String(30), default="AVAILABLE")  # AVAILABLE, LIMITED, DEPLETED
    contact_number = Column(String(50), default="1800-180-1234")
    email = Column(String(100), nullable=True)
    last_verified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
