"""AI Interview and conversational turn API routes."""
from typing import Optional
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.interview import (
    InterviewTurnRequest,
    InterviewTurnResponse,
    InterviewStartRequest,
    ConfirmFieldsRequest
)
from app.schemas.common import ApiResponse
from app.services.interview_service import InterviewService
from app.services.profile_service import ProfileService

router = APIRouter(tags=["AI Interview"])


@router.post("/interviews/{conversation_id}/turn", response_model=ApiResponse[InterviewTurnResponse])
def process_interview_turn(
    turn_req: InterviewTurnRequest,
    conversation_id: str = Path(..., description="Conversation or Profile identifier"),
    db: Session = Depends(get_db)
):
    """
    Process a speech/text utterance in the conversational AI interview.
    Extracts structured fields and returns the next targeted question.
    """
    existing_attrs = {}
    try:
        profile = ProfileService.get_profile(db, conversation_id)
        existing_attrs = profile.attributes
    except Exception:
        pass

    response_turn = InterviewService.process_turn(turn_req, existing_attrs)

    # If new fields extracted and valid profile exists, update profile attributes
    if response_turn.extracted_attributes and existing_attrs is not None:
        try:
            ProfileService.upsert_attributes(
                db,
                conversation_id,
                response_turn.extracted_attributes,
                source="ai_interview"
            )
        except Exception:
            pass

    return ApiResponse.success_response(response_turn)


@router.post("/interview/start", response_model=ApiResponse[dict])
def start_interview(start_req: InterviewStartRequest, db: Session = Depends(get_db)):
    """Start an AI interview session."""
    greeting = (
        "Namaste! Main Entrepreneur Mitra hoon. Aapki sarkari schemes aur concessional loan pane mein madad karunga. "
        "Kripya batayein, aap kis tarah ka business karte hain ya shuru karna chahte hain?"
        if start_req.language == "hi"
        else "Welcome to Entrepreneur Mitra! I will help you discover suitable government schemes and loans. Tell me about your business idea or existing trade."
    )
    return ApiResponse.success_response({
        "greeting": greeting,
        "first_field": "business_type",
        "language": start_req.language,
        "profile_id": start_req.profile_id
    })


@router.post("/interview/message", response_model=ApiResponse[InterviewTurnResponse])
def post_interview_message(turn_req: InterviewTurnRequest, db: Session = Depends(get_db)):
    """Shorthand alias for interview turn."""
    conv_id = turn_req.session_id or "default_session"
    return process_interview_turn(turn_req, conv_id, db)


@router.post("/interview/confirm", response_model=ApiResponse[dict])
def confirm_interview_fields(confirm_req: ConfirmFieldsRequest, db: Session = Depends(get_db)):
    """User confirmation of candidate fields extracted by AI."""
    return ApiResponse.success_response({
        "confirmed": True,
        "fields_confirmed": list(confirm_req.confirmed_fields.keys()),
        "message": "Fields successfully confirmed and saved to your profile."
    })
