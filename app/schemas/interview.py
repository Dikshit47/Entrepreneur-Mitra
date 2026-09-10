"""AI Interview schemas."""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class InterviewStartRequest(BaseModel):
    profile_id: Optional[str] = None
    language: str = "hi"


class InterviewTurnRequest(BaseModel):
    input_type: str = "text"  # text, voice
    text: Optional[str] = None
    user_message: Optional[str] = None
    message: Optional[str] = None
    language: Optional[str] = "en"
    session_id: Optional[str] = None  # alias for conversation
    conversation_id: Optional[str] = None
    existing_attributes: Optional[Dict[str, Any]] = None

    def get_text(self) -> str:
        return (self.text or self.user_message or self.message or "").strip()


class InterviewTurnResponse(BaseModel):
    assistant_message: str
    reply: str  # alias for assistant_message
    extracted_attributes: Dict[str, Any]
    extracted_fields: Dict[str, Any]  # alias for extracted_attributes
    next_required_field: Optional[str] = None
    next_question: Optional[str] = None
    requires_confirmation: bool = True
    uncertainties: List[str] = Field(default_factory=list)
    profile_completeness_pct: int = 0
    conversation_state: str = "in_progress"  # in_progress, awaiting_confirmation, ready_for_matching


class ConfirmFieldsRequest(BaseModel):
    confirmed_fields: Dict[str, Any]
