from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.membership import Membership
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    @staticmethod
    def list_memberships_for_transactions(db: Session) -> list[Membership]:
        return db.query(Membership).order_by(Membership.created_at.desc()).all()

    @staticmethod
    def create(db: Session, payload: TransactionCreate, current_user: User) -> Transaction:
        target_user = db.query(User).filter(User.id == payload.user_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")

        if current_user.role != "admin" and payload.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only create transactions for your own account")

        member = db.query(Membership).filter(Membership.id == payload.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Membership not found")

        transaction = Transaction(
            **payload.model_dump(),
            created_by=payload.user_id,
            transaction_date=datetime.now(timezone.utc),
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def list_for_user(db: Session, current_user: User) -> list[Transaction]:
        query = db.query(Transaction).order_by(Transaction.transaction_date.desc())
        if current_user.role == "admin":
            return query.all()
        return query.filter(Transaction.created_by == current_user.id).all()

    @staticmethod
    def update(db: Session, transaction_id: int, payload: TransactionUpdate, current_user: User) -> Transaction:
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        if current_user.role != "admin" and transaction.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this transaction")

        target_user = db.query(User).filter(User.id == payload.user_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")

        if current_user.role != "admin" and payload.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only update transactions for your own account")

        member = db.query(Membership).filter(Membership.id == payload.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Membership not found")

        for field, value in payload.model_dump().items():
            setattr(transaction, field, value)

        db.commit()
        db.refresh(transaction)
        return transaction
