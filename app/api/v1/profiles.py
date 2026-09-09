"""Entrepreneur Profile API routes."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_optional_current_user, get_current_user
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut
from app.schemas.common import ApiResponse
from app.services.profile_service import ProfileService

router = APIRouter(tags=["Profiles"])


@router.post("/profiles", response_model=ApiResponse[ProfileOut])
@router.post("/profile", response_model=ApiResponse[ProfileOut], include_in_schema=False)
def create_profile(
    prof_in: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """Create a new entrepreneur profile (supports anonymous MVP or authenticated user)."""
    user_id = current_user.id if current_user else None
    profile = ProfileService.create_profile(db, prof_in, user_id=user_id)
    return ApiResponse.success_response(profile)


@router.get("/profiles/{profile_id}", response_model=ApiResponse[ProfileOut])
def get_profile_by_id(profile_id: str, db: Session = Depends(get_db)):
    """Retrieve an entrepreneur profile by ID."""
    profile = ProfileService.get_profile(db, profile_id)
    return ApiResponse.success_response(profile)


@router.patch("/profiles/{profile_id}", response_model=ApiResponse[ProfileOut])
def update_profile_by_id(profile_id: str, update_in: ProfileUpdate, db: Session = Depends(get_db)):
    """Update profile attributes or preferred language."""
    profile = ProfileService.update_profile(db, profile_id, update_in)
    return ApiResponse.success_response(profile)


@router.get("/profile", response_model=ApiResponse[ProfileOut])
def get_my_profile(
    profile_id: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """Get current profile by query param or authenticated user."""
    if profile_id:
        profile = ProfileService.get_profile(db, profile_id)
        return ApiResponse.success_response(profile)
    if current_user and current_user.profiles:
        profile = ProfileService.get_profile(db, current_user.profiles[0].id)
        return ApiResponse.success_response(profile)
    
    # Create blank initial draft profile if none exists
    draft = ProfileService.create_profile(
        db,
        ProfileCreate(language="hi", attributes={}),
        user_id=current_user.id if current_user else None
    )
    return ApiResponse.success_response(draft)


@router.patch("/profile", response_model=ApiResponse[ProfileOut], include_in_schema=False)
def update_my_profile(
    update_in: ProfileUpdate,
    profile_id: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    target_id = profile_id
    if not target_id and current_user and current_user.profiles:
        target_id = current_user.profiles[0].id
    if not target_id:
        new_prof = ProfileService.create_profile(db, ProfileCreate(attributes=update_in.attributes), user_id=current_user.id if current_user else None)
        return ApiResponse.success_response(new_prof)
    profile = ProfileService.update_profile(db, target_id, update_in)
    return ApiResponse.success_response(profile)
