"""Saved Schemes (Bookmark) API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.api.deps import get_optional_current_user
from app.models.user import User
from app.models.scheme import Scheme
from app.models.saved_scheme import SavedScheme
from app.schemas.alert import SaveSchemeRequest, SavedSchemeOut
from app.schemas.common import ApiResponse
from app.utils.exceptions import NotFoundException

router = APIRouter(tags=["Saved Schemes"])


@router.post("/saved-schemes", response_model=ApiResponse[dict])
def save_scheme(
    req: SaveSchemeRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Bookmark/save a scheme for later access."""
    user = current_user or db.query(User).first()
    if not user:
        user = User(email="citizen.demo@mitra.gov.in", role="CITIZEN")
        db.add(user)
        db.commit()
        db.refresh(user)

    scheme = db.query(Scheme).filter(Scheme.scheme_id == req.scheme_id).first()
    if not scheme:
        raise NotFoundException(resource="Scheme", identifier=req.scheme_id)

    existing = db.query(SavedScheme).filter(
        SavedScheme.user_id == user.id,
        SavedScheme.scheme_id == req.scheme_id
    ).first()

    if not existing:
        saved = SavedScheme(user_id=user.id, scheme_id=req.scheme_id)
        db.add(saved)
        db.commit()

    return ApiResponse.success_response({
        "saved": True,
        "scheme_id": req.scheme_id,
        "message": "Scheme successfully bookmarked."
    })


@router.post("/schemes/{scheme_id}/save", response_model=ApiResponse[dict], include_in_schema=False)
def save_scheme_by_path(
    scheme_id: str = Path(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    return save_scheme(SaveSchemeRequest(scheme_id=scheme_id), db, current_user)


@router.delete("/schemes/{scheme_id}/save", response_model=ApiResponse[dict])
def unsave_scheme(
    scheme_id: str = Path(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Remove a saved scheme bookmark."""
    user = current_user or db.query(User).first()
    if user:
        saved = db.query(SavedScheme).filter(
            SavedScheme.user_id == user.id,
            SavedScheme.scheme_id == scheme_id
        ).first()
        if saved:
            db.delete(saved)
            db.commit()
    return ApiResponse.success_response({"removed": True, "scheme_id": scheme_id})


@router.get("/saved-schemes", response_model=ApiResponse[List[SavedSchemeOut]])
def list_saved_schemes(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """List all bookmarked schemes."""
    user = current_user or db.query(User).first()
    if not user:
        return ApiResponse.success_response([])

    saved_items = db.query(SavedScheme).options(
        joinedload(SavedScheme.scheme)
    ).filter(SavedScheme.user_id == user.id).all()

    out = []
    for s in saved_items:
        out.append(SavedSchemeOut(
            id=s.id,
            scheme_id=s.scheme_id,
            scheme_name=s.scheme.name if s.scheme else "",
            ministry=s.scheme.ministry if s.scheme else "",
            official_url=s.scheme.official_url if s.scheme else "",
            saved_at=s.saved_at
        ))
    return ApiResponse.success_response(out)
