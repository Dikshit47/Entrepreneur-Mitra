"""Application and Copilot schemas."""
from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ApplicationStepGuidance(BaseModel):
    step_number: int
    title: str
    status: str  # COMPLETED, CURRENT, PENDING
    description: str
    action_url: Optional[str] = None
    tips: List[str] = []


class ApplicationCreate(BaseModel):
    scheme_id: str
    selected_partner_id: Optional[str] = None
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: str
    scheme_id: str
    scheme_name: str
    selected_partner_id: Optional[str] = None
    partner_name: Optional[str] = None
    status: str
    copilot_step: int
    steps_guidance: List[ApplicationStepGuidance] = []
    official_application_url: str
    official_source_url: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
