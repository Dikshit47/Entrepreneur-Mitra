"""Authentication API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ApiResponse[Token])
def register(reg_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account."""
    token = AuthService.register(db, reg_in)
    return ApiResponse.success_response(token)


@router.post("/login", response_model=ApiResponse[Token])
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token."""
    token = AuthService.login(db, login_in)
    return ApiResponse.success_response(token)


@router.post("/logout", response_model=ApiResponse[dict])
def logout(current_user: User = Depends(get_current_user)):
    """Logout current user session."""
    return ApiResponse.success_response({"message": "Successfully logged out."})


@router.get("/me", response_model=ApiResponse[UserOut])
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Retrieve authenticated user details."""
    return ApiResponse.success_response(UserOut.model_validate(current_user))
