"""User model."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    auth_provider_id = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True, index=True)
    email = Column(String(120), nullable=True, unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    preferred_language = Column(String(10), default="hi")
    role = Column(String(20), default="CITIZEN")  # CITIZEN, ASSISTED_USER, ADMIN, AUDITOR
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    profiles = relationship("EntrepreneurProfile", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("UserDocument", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    saved_schemes = relationship("SavedScheme", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
