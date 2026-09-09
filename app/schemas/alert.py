"""Alerts and Saved Schemes schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    id: str
    scheme_id: Optional[str] = None
    alert_type: str
    title: str
    message: str
    read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SaveSchemeRequest(BaseModel):
    scheme_id: str


class SavedSchemeOut(BaseModel):
    id: str
    scheme_id: str
    scheme_name: str
    ministry: str
    official_url: str
    saved_at: datetime

    model_config = ConfigDict(from_attributes=True)
