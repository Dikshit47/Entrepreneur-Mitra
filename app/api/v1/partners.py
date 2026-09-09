"""Geo-spatial Partner Locator API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.partner import PartnerLocationOut, NearbyPartnerQuery
from app.schemas.common import ApiResponse
from app.services.partner_service import PartnerService

router = APIRouter(prefix="/partners", tags=["Partners & GIS"])


@router.get("/nearby", response_model=ApiResponse[List[PartnerLocationOut]])
def get_nearby_partners(
    lat: float = Query(..., ge=-90, le=90, description="Latitude of entrepreneur"),
    lng: float = Query(..., ge=-180, le=180, description="Longitude of entrepreneur"),
    scheme_id: Optional[str] = Query(None, description="Optional scheme ID to check category match"),
    radius_km: float = Query(50.0, gt=0, le=500, description="Search radius in kilometers"),
    category: Optional[str] = Query(None, description="Partner category filter"),
    db: Session = Depends(get_db)
):
    """
    Find authorized implementing channel partners near the entrepreneur's location.
    Calculates great-circle distance and verifies channel fund status.
    """
    query = NearbyPartnerQuery(
        latitude=lat,
        longitude=lng,
        scheme_id=scheme_id,
        radius_km=radius_km,
        category=category
    )
    partners = PartnerService.find_nearby_partners(db, query)
    return ApiResponse.success_response(partners)
