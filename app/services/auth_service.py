"""Authentication service."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.exceptions import InvalidInputException, AuthRequiredException


class AuthService:
    @staticmethod
    def register(db: Session, reg_in: UserRegister) -> Token:
        if not reg_in.email and not reg_in.phone:
            raise InvalidInputException("Either email or phone must be provided for registration.")

        # Check existing email
        if reg_in.email:
            existing = db.query(User).filter(User.email == reg_in.email).first()
            if existing:
                raise InvalidInputException("An account with this email already exists.")

        # Check existing phone
        if reg_in.phone:
            existing = db.query(User).filter(User.phone == reg_in.phone).first()
            if existing:
                raise InvalidInputException("An account with this phone number already exists.")

        user = User(
            email=reg_in.email,
            phone=reg_in.phone,
            hashed_password=hash_password(reg_in.password),
            preferred_language=reg_in.preferred_language,
            role="CITIZEN"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token({"sub": user.id, "role": user.role})
        return Token(access_token=token, token_type="bearer", user=UserOut.model_validate(user))

    @staticmethod
    def login(db: Session, login_in: UserLogin) -> Token:
        identifier = login_in.email_or_phone.strip()
        user = db.query(User).filter(
            (User.email == identifier) | (User.phone == identifier)
        ).first()

        if not user or not user.hashed_password or not verify_password(login_in.password, user.hashed_password):
            raise AuthRequiredException("Invalid credentials. Please check your email/phone and password.")

        token = create_access_token({"sub": user.id, "role": user.role})
        return Token(access_token=token, token_type="bearer", user=UserOut.model_validate(user))
