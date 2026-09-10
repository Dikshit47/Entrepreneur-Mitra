"""Explainable Guidance and Citizen Assistant API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.assistant import AssistantExplainRequest, AssistantExplainResponse
from app.schemas.common import ApiResponse
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/assistant", tags=["Citizen Assistant & Guidance"])


@router.post("/explain", response_model=ApiResponse[AssistantExplainResponse])
def explain_scheme_guidance(req: AssistantExplainRequest, db: Session = Depends(get_db)):
    """
    Generate grounded natural-language explanation of eligibility.
    Grounded strictly in deterministic rule evaluation; never modifies the underlying decision.
    """
    explanation = AssistantService.explain_eligibility(db, req)
    return ApiResponse.success_response(explanation)
