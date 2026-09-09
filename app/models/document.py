"""User Document model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
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
    extracted_data_json = Column(Text, nullable=True)  # Candidate fields requiring user confirmation
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="documents")
