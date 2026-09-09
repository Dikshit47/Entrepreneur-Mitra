"""Alerts and Scheme Change Notifications API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_optional_current_user
from app.models.user import User
from app.models.alert import Alert
from app.schemas.alert import AlertOut
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=ApiResponse[List[AlertOut]])
def get_alerts(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Retrieve notifications, scheme policy updates, and application deadlines."""
    user = current_user or db.query(User).first()
    alerts = []
    if user:
        alerts = db.query(Alert).filter(Alert.user_id == user.id).order_by(Alert.created_at.desc()).all()

    # If user has no alerts, provide demo government notifications
    if not alerts:
        return ApiResponse.success_response([
            {
                "id": "alert_01",
                "scheme_id": "NBCFDC-GTL-001",
                "alert_type": "SCHEME_UPDATE",
                "title": "MoSJE Concessional Loan Window Open",
                "message": "NBCFDC State Channelising Agencies have updated credit allocation for UP and Maharashtra.",
                "read": False,
                "created_at": "2026-09-01T10:00:00Z"
            },
            {
                "id": "alert_02",
                "scheme_id": "STANDUP-INDIA-001",
                "alert_type": "DEADLINE",
                "title": "Subsidy Margin Relief",
                "message": "Promoter contribution margin reduced to 5% for qualifying SC/ST greenfield projects.",
                "read": True,
                "created_at": "2026-08-25T14:30:00Z"
            }
        ])

    out = []
    for a in alerts:
        out.append(AlertOut(
            id=a.id,
            scheme_id=a.scheme_id,
            alert_type=a.alert_type,
            title=a.title,
            message=a.message,
            read=a.read_at is not None,
            created_at=a.created_at
        ))
    return ApiResponse.success_response(out)
