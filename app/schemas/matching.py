"""Scheme Matching and Ranking schemas."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ScoreBreakdown(BaseModel):
    eligibility_completeness: float = Field(..., description="Weight 35%")
    purpose_fit: float = Field(..., description="Weight 25%")
    financial_fit: float = Field(..., description="Weight 15%")
    geography_fit: float = Field(..., description="Weight 10%")
    document_readiness: float = Field(..., description="Weight 10%")
    user_preference: float = Field(..., description="Weight 5%")


class MatchItem(BaseModel):
    scheme_id: str
    scheme_name: str
    ministry: str
    scheme_type: str
    status: str  # ELIGIBLE, PARTIALLY_ELIGIBLE, NOT_ELIGIBLE, etc.
    match_score: int  # 0 - 100
    score_breakdown: ScoreBreakdown
    passed: List[str] = []
    missing: List[str] = []
    why_matched: List[str] = []
    missing_requirements: List[str] = []
    estimated_max_loan: Optional[float] = None
    interest_rate: Optional[float] = None
    official_url: str


class MatchRequest(BaseModel):
    profile_id: str


class MatchResponse(BaseModel):
    profile_id: str
    results: List[MatchItem]
    total_evaluated: int


class MatchExplanationCriterion(BaseModel):
    label: str
    result: str  # PASS, FAIL, UNKNOWN
    reason: str
    source_id: Optional[str] = None


class MatchExplanationOut(BaseModel):
    scheme_id: str
    scheme_name: str
    decision: str
    summary: str
    criteria: List[MatchExplanationCriterion]
    official_url: str
    last_verified_at: str
