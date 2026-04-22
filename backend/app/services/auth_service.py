from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import access_token_expires_delta
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def register_user(db: Session, payload: UserCreate) -> User:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            role="user",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> dict:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")

        access_token = create_access_token(
            subject=user.email,
            expires_delta=access_token_expires_delta(),
            extra_claims={"role": user.role},
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role,
            "full_name": user.full_name,
        }
