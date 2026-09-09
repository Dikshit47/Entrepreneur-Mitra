"""Explainable AI schemas."""
from typing import List
from pydantic import BaseModel


class AIExplainRequest(BaseModel):
    scheme_id: str
    profile_id: str
    language: str = "hi"


class AIExplainResponse(BaseModel):
    scheme_id: str
    language: str
    decision: str
    plain_explanation: str
    key_points: List[str]
    next_steps: List[str]
    grounding_source: str
