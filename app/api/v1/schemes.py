"""Scheme Knowledge Base API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.scheme import SchemeOut, SchemeDetailOut
from app.schemas.common import ApiResponse
from app.services.scheme_service import SchemeService

router = APIRouter(prefix="/schemes", tags=["Schemes"])


@router.get("", response_model=ApiResponse[List[SchemeOut]])
def list_schemes(
    status: Optional[str] = Query("ACTIVE"),
    scheme_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all verified government schemes with optional filtering."""
    schemes = SchemeService.get_schemes(db, status=status, scheme_type=scheme_type, search=search)
    return ApiResponse.success_response(schemes)


@router.get("/{scheme_id}", response_model=ApiResponse[SchemeDetailOut])
def get_scheme_details(scheme_id: str, db: Session = Depends(get_db)):
    """Retrieve full details of a scheme including rules, benefits, and verified official sources."""
    scheme = SchemeService.get_scheme_by_id(db, scheme_id)
    return ApiResponse.success_response(scheme)


@router.get("/{scheme_id}/application-steps", response_model=ApiResponse[dict])
def get_scheme_application_steps(scheme_id: str, db: Session = Depends(get_db)):
    """Get authoritative application guidance and steps for a specific scheme."""
    scheme = SchemeService.get_scheme_by_id(db, scheme_id)
    
    steps = [
        {
            "step_number": 1,
            "title": "Check Eligibility & Documents",
            "description": "Ensure your income certificate, caste certificate (if applicable), and project summary are ready.",
            "status": "COMPLETED"
        },
        {
            "step_number": 2,
            "title": "Fill Official Application Form",
            "description": f"Visit official government portal: {scheme.application_url}",
            "action_url": scheme.application_url,
            "status": "CURRENT"
        },
        {
            "step_number": 3,
            "title": "Channel Partner / Bank Verification",
            "description": "Submit hard copies to the designated State Channelising Agency (SCA) or authorized bank branch.",
            "status": "PENDING"
        },
        {
            "step_number": 4,
            "title": "Sanction & Disbursal",
            "description": "Track application status through your applicant login on the official portal.",
            "status": "PENDING"
        }
    ]

    return ApiResponse.success_response({
        "scheme_id": scheme.scheme_id,
        "scheme_name": scheme.name,
        "official_application_url": scheme.application_url,
        "official_source_url": scheme.official_url,
        "steps": steps
    })
