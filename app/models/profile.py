"""Entrepreneur Profile and Profile Attribute models."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EntrepreneurProfile(Base):
    __tablename__ = "entrepreneur_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    profile_version = Column(Integer, default=1)
    status = Column(String(20), default="draft")  # draft, confirmed, archived
    preferred_language = Column(String(10), default="hi")
    confirmed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="profiles")
    attributes = relationship("ProfileAttribute", back_populates="profile", cascade="all, delete-orphan")


class ProfileAttribute(Base):
    __tablename__ = "profile_attributes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String(36), ForeignKey("entrepreneur_profiles.id"), nullable=False, index=True)
    attribute_key = Column(String(60), nullable=False, index=True)
    attribute_value = Column(String(255), nullable=False)
    data_type = Column(String(20), default="string")  # string, number, boolean
    source = Column(String(30), default="user_input")  # user_input, ai_interview, document_ocr
    confidence = Column(Float, default=1.0)
    user_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    profile = relationship("EntrepreneurProfile", back_populates="attributes")
