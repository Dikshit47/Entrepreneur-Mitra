"""Audit Log and Eligibility Evaluation trace records."""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text
from app.database import Base


class EligibilityEvaluation(Base):
    __tablename__ = "eligibility_evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String(36), nullable=False, index=True)
    scheme_id = Column(String(50), nullable=False, index=True)
    decision = Column(String(30), nullable=False)  # ELIGIBLE, NOT_ELIGIBLE, PARTIALLY_ELIGIBLE, NEEDS_VERIFICATION, INSUFFICIENT_INFORMATION
    rule_trace_json = Column(Text, nullable=False)
    engine_version = Column(String(20), default="v1.0")
    evaluated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True, index=True)
    actor_type = Column(String(30), default="CITIZEN")  # CITIZEN, SYSTEM, ADMIN
    action = Column(String(60), nullable=False)  # CREATE_PROFILE, RUN_EVALUATION, UPLOAD_DOC, SIMULATE_WHATIF
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(50), nullable=False)
    metadata_json = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
