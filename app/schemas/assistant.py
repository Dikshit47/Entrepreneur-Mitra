"""Assistant and Explanation Schemas."""
from typing import List, Optional
from pydantic import BaseModel, Field


class AssistantExplainRequest(BaseModel):
    profile_id: str = Field(..., description="Entrepreneur Profile ID")
    scheme_id: str = Field(..., description="Government Scheme ID")
    language: str = Field("hi", description="Language preference (hi, en, hinglish, mr, bn, etc.)")


class AssistantExplainResponse(BaseModel):
    scheme_id: str
    summary: str
    key_factors: List[str]
    next_steps: List[str]
    language: str
    grounded: bool = True
