"""Scheme Knowledge Base models."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Scheme(Base):
    __tablename__ = "schemes"

    scheme_id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    short_name = Column(String(50), nullable=True)
    ministry = Column(String(150), nullable=False)
    department = Column(String(150), nullable=True)
    scheme_type = Column(String(50), default="CREDIT_LOAN")  # CREDIT_LOAN, SUBSIDY, SKILL, COMPOSITE
    target_group = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, STALE, ARCHIVED
    geography_scope = Column(String(50), default="PAN_INDIA")
    official_url = Column(String(300), nullable=False)
    application_url = Column(String(300), nullable=False)
    helpline = Column(String(100), nullable=True)
    source_confidence = Column(String(20), default="VERIFIED")  # VERIFIED, HIGH, PARTIAL, UNCERTAIN
    last_verified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    data_version = Column(String(20), default="v1.0")
    effective_from = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    effective_to = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    rules = relationship("SchemeRule", back_populates="scheme", cascade="all, delete-orphan")
    benefits = relationship("SchemeBenefit", back_populates="scheme", cascade="all, delete-orphan")
    required_documents = relationship("DocumentRequirement", back_populates="scheme", cascade="all, delete-orphan")
    sources = relationship("SchemeSource", back_populates="scheme", cascade="all, delete-orphan")


class SchemeRule(Base):
    __tablename__ = "scheme_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False, index=True)
    rule_id = Column(String(50), nullable=False, index=True)
    field_name = Column(String(60), nullable=False, index=True)
    operator = Column(String(20), nullable=False)  # <=, >=, ==, !=, in, contains
    expected_value = Column(String(255), nullable=False)
    value_unit = Column(String(30), nullable=True)  # INR, YEARS, %
    condition_group = Column(String(30), default="PRIMARY")
    rule_type = Column(String(20), default="hard")  # hard, soft, conditional
    explanation_template = Column(Text, nullable=False)
    source_reference_id = Column(String(50), nullable=True)
    version = Column(Integer, default=1)
    effective_from = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    effective_to = Column(DateTime, nullable=True)

    scheme = relationship("Scheme", back_populates="rules")


class SchemeBenefit(Base):
    __tablename__ = "scheme_benefits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False, index=True)
    benefit_type = Column(String(50), default="CONCESSIONAL_LOAN")  # CONCESSIONAL_LOAN, SUBSIDY, MARGIN_MONEY
    min_value = Column(Float, default=0.0)
    max_value = Column(Float, default=0.0)
    percentage = Column(Float, nullable=True)
    interest_rate = Column(Float, default=5.0)  # Concessional rate e.g. 4.0 - 6.0%
    tenure_months = Column(Integer, default=60)
    moratorium_months = Column(Integer, default=6)
    description = Column(Text, nullable=False)
    source_reference_id = Column(String(50), nullable=True)

    scheme = relationship("Scheme", back_populates="benefits")


class DocumentRequirement(Base):
    __tablename__ = "document_requirements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False, index=True)
    document_type = Column(String(60), nullable=False)  # INCOME_CERTIFICATE, CASTE_CERTIFICATE, AADHAAR, PROJECT_REPORT
    mandatory = Column(Boolean, default=True)
    acceptable_variants = Column(String(255), default="Standard Government Issued Certificate")
    verification_level = Column(String(30), default="GOVERNMENT_VERIFIED")
    source_reference_id = Column(String(50), nullable=True)

    scheme = relationship("Scheme", back_populates="required_documents")


class SchemeSource(Base):
    __tablename__ = "scheme_sources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False, index=True)
    publisher = Column(String(150), nullable=False)
    source_url = Column(String(300), nullable=False)
    source_type = Column(String(50), default="OFFICIAL_PORTAL")  # OFFICIAL_PORTAL, GAZETTE, GUIDELINE_PDF
    retrieved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    verified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    content_hash = Column(String(64), default="")
    verification_status = Column(String(30), default="VERIFIED")

    scheme = relationship("Scheme", back_populates="sources")
