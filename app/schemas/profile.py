"""Entrepreneur Profile schemas."""
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class AttributeSchema(BaseModel):
    key: str
    value: Any
    data_type: str = "string"
    source: str = "user_input"
    confidence: float = 1.0
    user_confirmed: bool = False


class ProfileCreate(BaseModel):
    language: str = "hi"
    attributes: Dict[str, Any] = Field(default_factory=dict)


class ProfileUpdate(BaseModel):
    language: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class ProfileOut(BaseModel):
    profile_id: str
    user_id: Optional[str] = None
    status: str
    language: str
    attributes: Dict[str, Any]
    attribute_details: Optional[List[AttributeSchema]] = None
    completeness_pct: int
    confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
