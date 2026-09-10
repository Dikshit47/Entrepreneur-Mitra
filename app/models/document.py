"""User Document model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class UserDocument(Base):
    __tablename__ = "user_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    document_type = Column(String(60), nullable=False)  # INCOME_CERTIFICATE, CASTE_CERTIFICATE, AADHAAR, PROJECT_REPORT
    original_filename = Column(String(255), nullable=False)
    storage_key = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    checksum = Column(String(64), nullable=False)
    ocr_status = Column(String(30), default="UPLOADED")  # UPLOADED, PROCESSING, EXTRACTED, FAILED
    document_status = Column(String(30), default="NEEDS_REVIEW")  # NEEDS_REVIEW, USER_CONFIRMED, REJECTED
    
    # Document Trust & Verification Hierarchy attributes (PART 10-15)
    verification_status = Column(String(40), default="UNVERIFIED")  # UNVERIFIED, VERIFICATION_PENDING, DIGILOCKER_VERIFIED, ISSUER_VERIFIED, MANUAL_REVIEW, VERIFICATION_FAILED, EXPIRED
    source = Column(String(40), default="MANUAL_UPLOAD")  # DIGILOCKER_ISSUER, MANUAL_UPLOAD, OCR_EXTRACTION, USER_PROVIDED
    verification_method = Column(String(60), nullable=True)  # DIGILOCKER_OAUTH, MANUAL_REVIEW, OCR_CHECKSUM
    issuer = Column(String(150), nullable=True)  # e.g., 'Revenue Department, Govt of Uttar Pradesh'
    issued_date = Column(String(50), nullable=True)
    expiry_date = Column(String(50), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    verification_reference = Column(String(100), nullable=True)  # DigiLocker URI / Doc Ref No
    is_sandbox = Column(Boolean, default=True)  # Clearly labels mock/sandbox mode for SIH Demo safety

    extracted_data_json = Column(Text, nullable=True)  # Candidate fields requiring user confirmation
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="documents")
