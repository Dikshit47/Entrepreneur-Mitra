"""Geo-spatial Partner schemas."""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PartnerLocationOut(BaseModel):
    partner_id: str
    name: str
    partner_type: str
    scheme_categories: str
    distance_km: float
    category_match: bool
    status: str
    fund_utilisation_status: str
    address: str
    district: str
    state: str
    pincode: Optional[str] = None
    contact_number: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class NearbyPartnerQuery(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    scheme_id: Optional[str] = None
    radius_km: float = Field(default=50.0, gt=0, le=500)
    category: Optional[str] = None
