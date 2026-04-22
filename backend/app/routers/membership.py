from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.membership import Membership
from app.models.user import User
from app.schemas.membership import MembershipCreate, MembershipResponse, MembershipUpdate

router = APIRouter()


@router.post("/", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
def create_membership(
    payload: MembershipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = Membership(**payload.model_dump(), created_by=current_user.id)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get("/", response_model=list[MembershipResponse])
def list_memberships(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Membership).order_by(Membership.created_at.desc()).all()


@router.put("/{membership_id}", response_model=MembershipResponse)
def update_membership(
    membership_id: int,
    payload: MembershipUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    for field, value in payload.model_dump().items():
        setattr(membership, field, value)

    db.commit()
    db.refresh(membership)
    return membership
