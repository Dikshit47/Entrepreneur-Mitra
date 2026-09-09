"""Explainable AI API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.ai import AIExplainRequest, AIExplainResponse
from app.schemas.common import ApiResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["Explainable AI"])


@router.post("/explain", response_model=ApiResponse[AIExplainResponse])
def explain_scheme_ai(req: AIExplainRequest, db: Session = Depends(get_db)):
    """
    Generate grounded, natural-language explanation of eligibility.
    Grounded strictly in deterministic rule evaluation; never modifies the underlying decision.
    """
    explanation = AIService.explain_eligibility(db, req)
    return ApiResponse.success_response(explanation)
