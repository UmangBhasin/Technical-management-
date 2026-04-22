from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.membership import MembershipActionUpdate, MembershipCreate, MembershipResponse
from app.services.membership_service import MembershipService

router = APIRouter()


@router.post("/", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
def create_membership(
    payload: MembershipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return MembershipService.create(db, payload, current_user.id)


@router.get("/", response_model=list[MembershipResponse])
def list_memberships(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return MembershipService.list_all(db)


@router.get("/{membership_id}", response_model=MembershipResponse)
def get_membership_by_id(membership_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return MembershipService.get_by_id(db, membership_id)


@router.put("/{membership_id}", response_model=MembershipResponse)
def update_membership(
    membership_id: int,
    payload: MembershipActionUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return MembershipService.update(db, membership_id, payload)
