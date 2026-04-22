from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.membership import Membership
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate

router = APIRouter()


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = db.query(Membership).filter(Membership.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Membership not found")

    transaction = Transaction(
        **payload.model_dump(),
        created_by=current_user.id,
        transaction_date=datetime.now(timezone.utc),
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Transaction).order_by(Transaction.transaction_date.desc())
    if current_user.role == "admin":
        return query.all()
    return query.filter(Transaction.created_by == current_user.id).all()


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if current_user.role != "admin" and transaction.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this transaction")

    member = db.query(Membership).filter(Membership.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Membership not found")

    for field, value in payload.model_dump().items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)
    return transaction
