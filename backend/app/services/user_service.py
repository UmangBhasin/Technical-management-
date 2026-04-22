from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import ADMIN_DEFAULT_EMAIL
from app.core.security import hash_password
from app.models.membership import Membership
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.user import UserMaintenanceCreate, UserMaintenanceUpdate


class UserService:
    @staticmethod
    def list_users(db: Session) -> list[User]:
        return db.query(User).order_by(User.created_at.desc()).all()

    @staticmethod
    def create_user_from_maintenance(db: Session, payload: UserMaintenanceCreate) -> User:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            role=payload.role,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user_from_maintenance(db: Session, user_id: int, payload: UserMaintenanceUpdate) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        existing_email_user = db.query(User).filter(User.email == payload.email, User.id != user_id).first()
        if existing_email_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user.full_name = payload.full_name
        user.email = payload.email
        user.role = payload.role
        user.is_active = payload.is_active
        user.password_hash = hash_password(payload.password)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user_from_maintenance(db: Session, user_id: int, current_user_id: int) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.id == current_user_id:
            raise HTTPException(status_code=400, detail="You cannot delete your own account")

        if user.email == ADMIN_DEFAULT_EMAIL:
            raise HTTPException(status_code=400, detail="Default admin user cannot be deleted")

        has_transactions = db.query(Transaction.id).filter(Transaction.created_by == user.id).first()
        has_memberships = db.query(Membership.id).filter(Membership.created_by == user.id).first()
        if has_transactions or has_memberships:
            raise HTTPException(
                status_code=409,
                detail="User is used by reports or transactions and cannot be deleted",
            )

        db.delete(user)
        db.commit()
