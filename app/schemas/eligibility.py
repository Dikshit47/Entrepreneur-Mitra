"""Eligibility Engine and What-If Simulator schemas."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CriterionResult(BaseModel):
    rule_id: str
    field_name: str
    operator: str
    expected_value: Any
    user_value: Any
    result: str  # PASS, FAIL, UNKNOWN
    rule_type: str  # hard, soft, conditional
    reason: str
    source_id: Optional[str] = None
    trust_level: str = "USER_PROVIDED"  # VERIFIED, USER_PROVIDED, UNKNOWN, CONFLICTING


class SchemeEligibilityResult(BaseModel):
    scheme_id: str
    scheme_name: Optional[str] = None
    status: str  # ELIGIBLE, NOT_ELIGIBLE, PARTIALLY_ELIGIBLE, NEEDS_VERIFICATION, INSUFFICIENT_INFORMATION
    criteria: List[CriterionResult] = []
    matched_rules: List[str] = []
    failed_rules: List[str] = []
    missing_information: List[str] = []
    passed: List[str] = []  # alias for user summary
    missing: List[str] = []  # alias for user summary
    summary_explanation: Optional[str] = None


class EligibilityCheckRequest(BaseModel):
    profile_id: str
    scheme_ids: Optional[List[str]] = None


class WhatIfSimulateRequest(BaseModel):
    profile_id: str
    scheme_id: Optional[str] = None
    hypothetical_changes: Dict[str, Any]


class WhatIfResultOut(BaseModel):
    is_hypothetical: bool = True
    profile_id: str
    scheme_id: str
    original: Dict[str, Any]  # { "decision": "...", "status": "..." }
    simulated: Dict[str, Any]  # { "decision": "...", "status": "..." }
    changed_rules: List[str]
    explanation: str
    warning: str = "This is a hypothetical simulation. Do not provide false information in actual applications."
