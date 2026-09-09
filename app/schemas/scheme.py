"""Scheme schemas."""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SchemeRuleOut(BaseModel):
    rule_id: str
    field_name: str
    operator: str
    expected_value: str
    value_unit: Optional[str] = None
    rule_type: str
    explanation_template: str

    model_config = ConfigDict(from_attributes=True)


class SchemeBenefitOut(BaseModel):
    benefit_type: str
    min_value: float
    max_value: float
    percentage: Optional[float] = None
    interest_rate: float
    tenure_months: int
    moratorium_months: int
    description: str

    model_config = ConfigDict(from_attributes=True)


class DocumentRequirementOut(BaseModel):
    document_type: str
    mandatory: bool
    acceptable_variants: str
    verification_level: str

    model_config = ConfigDict(from_attributes=True)


class SchemeSourceOut(BaseModel):
    publisher: str
    source_url: str
    source_type: str
    verified_at: datetime
    verification_status: str

    model_config = ConfigDict(from_attributes=True)


class SchemeOut(BaseModel):
    scheme_id: str
    name: str
    short_name: Optional[str] = None
    ministry: str
    department: Optional[str] = None
    scheme_type: str
    target_group: Optional[str] = None
    description: str
    status: str
    official_url: str
    application_url: str
    helpline: Optional[str] = None
    source_confidence: str
    last_verified_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SchemeDetailOut(SchemeOut):
    rules: List[SchemeRuleOut] = []
    benefits: List[SchemeBenefitOut] = []
    required_documents: List[DocumentRequirementOut] = []
    sources: List[SchemeSourceOut] = []
