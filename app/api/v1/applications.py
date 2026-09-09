"""Application Copilot and Tracking API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.api.deps import get_current_user, get_optional_current_user
from app.models.user import User
from app.models.application import Application
from app.models.scheme import Scheme
from app.schemas.application import ApplicationCreate, ApplicationOut, ApplicationStepGuidance
from app.schemas.common import ApiResponse
from app.utils.exceptions import NotFoundException, InvalidInputException

router = APIRouter(prefix="/applications", tags=["Application Copilot"])


def _build_application_out(app: Application) -> ApplicationOut:
    scheme = app.scheme
    partner_name = app.partner.partner_name if app.partner else None

    steps = [
        ApplicationStepGuidance(
            step_number=1,
            title="Eligibility & Profile Check",
            status="COMPLETED" if app.copilot_step >= 1 else "PENDING",
            description="Profile verified against published rules.",
            tips=["Ensure all income and category certificates match your profile."]
        ),
        ApplicationStepGuidance(
            step_number=2,
            title="Document Preparation",
            status="COMPLETED" if app.copilot_step >= 2 else ("CURRENT" if app.copilot_step == 1 else "PENDING"),
            description="Collect mandatory scheme documents.",
            tips=["Keep digital copies of Aadhaar, Income Certificate, and Project Summary ready."]
        ),
        ApplicationStepGuidance(
            step_number=3,
            title="Form Submission through Official Portal",
            status="COMPLETED" if app.copilot_step >= 3 else ("CURRENT" if app.copilot_step == 2 else "PENDING"),
            description=f"Submit details on the government portal: {scheme.application_url}",
            action_url=scheme.application_url,
            tips=["Never share OTPs or passwords with unofficial agents."]
        ),
        ApplicationStepGuidance(
            step_number=4,
            title="Channel Partner Visit & Document Verification",
            status="COMPLETED" if app.copilot_step >= 4 else ("CURRENT" if app.copilot_step == 3 else "PENDING"),
            description=f"Visit {partner_name or 'designated SCA/Bank branch'} with your original documents.",
            tips=["Carry physical application acknowledgment and original identity cards."]
        ),
        ApplicationStepGuidance(
            step_number=5,
            title="Sanction & Disbursal Tracking",
            status="COMPLETED" if app.copilot_step >= 5 else "PENDING",
            description="Track disbursal and concessional interest subvention.",
            tips=["Keep your loan application reference number safe."]
        )
    ]

    return ApplicationOut(
        id=app.id,
        scheme_id=app.scheme_id,
        scheme_name=scheme.name if scheme else "Unknown Scheme",
        selected_partner_id=app.selected_partner_id,
        partner_name=partner_name,
        status=app.status,
        copilot_step=app.copilot_step,
        steps_guidance=steps,
        official_application_url=scheme.application_url if scheme else "",
        official_source_url=scheme.official_url if scheme else "",
        notes=app.notes,
        created_at=app.created_at,
        updated_at=app.updated_at
    )


@router.post("", response_model=ApiResponse[ApplicationOut])
def create_application(
    app_in: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Initiate a guided scheme application."""
    user = current_user
    if not user:
        # For demo purposes, pick the first user or create a guest user
        user = db.query(User).first()
        if not user:
            user = User(email="guest.entrepreneur@mitra.gov.in", role="CITIZEN")
            db.add(user)
            db.commit()
            db.refresh(user)

    scheme = db.query(Scheme).filter(Scheme.scheme_id == app_in.scheme_id).first()
    if not scheme:
        raise NotFoundException(resource="Scheme", identifier=app_in.scheme_id)

    app = Application(
        user_id=user.id,
        scheme_id=app_in.scheme_id,
        selected_partner_id=app_in.selected_partner_id,
        status="DRAFT",
        copilot_step=1,
        notes=app_in.notes
    )
    db.add(app)
    db.commit()
    db.refresh(app)

    return ApiResponse.success_response(_build_application_out(app))


@router.get("", response_model=ApiResponse[List[ApplicationOut]])
def list_applications(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """List tracked applications."""
    query = db.query(Application).options(
        joinedload(Application.scheme),
        joinedload(Application.partner)
    )
    if current_user:
        query = query.filter(Application.user_id == current_user.id)
    apps = query.order_by(Application.created_at.desc()).all()
    return ApiResponse.success_response([_build_application_out(a) for a in apps])


@router.get("/{application_id}", response_model=ApiResponse[ApplicationOut])
def get_application(application_id: str, db: Session = Depends(get_db)):
    """Get single application with full Copilot step guidance."""
    app = db.query(Application).options(
        joinedload(Application.scheme),
        joinedload(Application.partner)
    ).filter(Application.id == application_id).first()

    if not app:
        raise NotFoundException(resource="Application", identifier=application_id)

    return ApiResponse.success_response(_build_application_out(app))
