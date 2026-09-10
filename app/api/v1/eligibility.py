"""Eligibility and What-If Simulator API routes."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.eligibility import (
    EligibilityCheckRequest,
    SchemeEligibilityResult,
    WhatIfSimulateRequest,
    WhatIfResultOut
)
from app.schemas.common import ApiResponse
from app.services.eligibility_service import EligibilityService

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])


@router.post("/check", response_model=ApiResponse[List[SchemeEligibilityResult]])
def check_eligibility(
    req: EligibilityCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluate deterministic scheme eligibility for a given entrepreneur profile.
    Returns traceable criteria evaluation with exact pass/fail reasons.
    """
    results = EligibilityService.evaluate_schemes_for_profile(
        db,
        profile_id=req.profile_id,
        scheme_ids=req.scheme_ids
    )
    return ApiResponse.success_response(results)


@router.post("/simulate", response_model=ApiResponse[WhatIfResultOut])
def simulate_what_if(
    req: WhatIfSimulateRequest,
    db: Session = Depends(get_db)
):
    """
    Simulate hypothetical eligibility when attributes change (e.g. income, project cost).
    Zero database mutation; clearly flagged as hypothetical.
    """
    simulation = EligibilityService.simulate_what_if(
        db,
        profile_id=req.profile_id,
        hypothetical_changes=req.get_changes(),
        scheme_id=req.scheme_id
    )
    return ApiResponse.success_response(simulation)
