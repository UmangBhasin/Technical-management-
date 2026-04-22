from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.membership import Membership
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.get("/memberships", response_model=list[dict])
def list_membership_options(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    memberships: list[Membership] = TransactionService.list_memberships_for_transactions(db)
    return [
        {
            "id": m.id,
            "member_name": m.member_name,
            "membership_type": m.membership_type,
            "status": m.status,
        }
        for m in memberships
    ]


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService.create(db, payload, current_user)


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return TransactionService.list_for_user(db, current_user)


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService.update(db, transaction_id, payload, current_user)
