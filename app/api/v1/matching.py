"""Scheme Matching and Ranking API routes."""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.matching import MatchRequest, MatchResponse, MatchExplanationOut
from app.schemas.common import ApiResponse
from app.services.matching_service import MatchingService

router = APIRouter(tags=["Matching"])


@router.post("/matches", response_model=ApiResponse[MatchResponse])
@router.post("/matching", response_model=ApiResponse[MatchResponse], include_in_schema=False)
def match_schemes(req: MatchRequest, db: Session = Depends(get_db)):
    """
    Match and rank government schemes for an entrepreneur profile
    using the transparent 6-factor weighting model.
    """
    matches = MatchingService.match_schemes_for_profile(db, req.profile_id)
    return ApiResponse.success_response(matches)


@router.get("/matching/results", response_model=ApiResponse[MatchResponse])
def get_matching_results(profile_id: str = Query(..., description="Entrepreneur Profile ID"), db: Session = Depends(get_db)):
    """Get matched schemes by query parameter."""
    matches = MatchingService.match_schemes_for_profile(db, profile_id)
    return ApiResponse.success_response(matches)


@router.get("/matches/{scheme_id}/explanation", response_model=ApiResponse[MatchExplanationOut])
def explain_scheme_match(
    scheme_id: str = Path(...),
    profile_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Return structured rule trace explaining exactly WHY a scheme was matched or rejected.
    """
    explanation = MatchingService.explain_match(db, scheme_id, profile_id)
    return ApiResponse.success_response(explanation)
